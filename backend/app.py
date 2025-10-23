"""
FastAPI application with RQ job queue integration
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from redis import Redis
from rq import Queue
from rq.job import Job
import pathlib
import json

from .database import get_db, init_db
from .models import Submission, TestResult
from .config import settings
from .logging_config import setup_logging, get_logger
from .validators import validate_submission_request
from .services.problem_service import problem_service
from .services.submission_service import submission_service
from .schemas import (
    SubmissionRequest,
    SubmissionResponse,
    ResultResponse,
    TestResultSchema,
    AdminSummary,
    SubmissionsListResponse
)

# Setup logging
logger = get_logger(__name__)

app = FastAPI(title="Python Playground Suite")

# CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis y RQ
redis_conn = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=False
)
queue = Queue("submissions", connection=redis_conn)


@app.on_event("startup")
def startup_event():
    """Initialize database and logging on startup"""
    setup_logging()
    logger.info("Starting Python Playground API", extra={"version": "2.0.0"})
    init_db()
    logger.info("Database initialized successfully")


@app.get("/api/problems")
def list_problems() -> Dict[str, Any]:
    """List all available problems with metadata and prompts"""
    logger.info("Fetching list of problems")
    return problem_service.list_all()


@app.post("/api/submit", response_model=SubmissionResponse)
def submit(req: SubmissionRequest, db: Session = Depends(get_db)):
    """Submit code for evaluation - enqueues job"""
    logger.info(f"Received submission for problem: {req.problem_id}")

    # Validate request
    validate_submission_request(req)

    # Create submission in DB
    submission = submission_service.create_submission(
        db=db,
        problem_id=req.problem_id,
        code=req.code,
        student_id=req.student_id
    )

    # Enqueue job in RQ
    job = queue.enqueue(
        "worker.tasks.run_submission_in_sandbox",
        submission_id=submission.id,
        problem_id=req.problem_id,
        code=req.code,
        timeout_sec=req.timeout_sec,
        memory_mb=req.memory_mb,
        job_timeout="5m"
    )

    # Update submission with job_id
    submission_service.update_job_id(db=db, submission_id=submission.id, job_id=job.id)

    return SubmissionResponse(
        job_id=job.id,
        status="queued",
        message="Submission enqueued successfully"
    )


@app.get("/api/result/{job_id}")
def get_result(job_id: str, db: Session = Depends(get_db)):
    """Get result of a submission by job_id"""
    # Find submission in DB
    submission = submission_service.get_by_job_id(db=db, job_id=job_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    # If completed, return full result
    if submission.status in ["completed", "failed", "timeout"]:
        return submission_service.get_result_dict(submission)

    # If in progress, query RQ job
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        return {
            "job_id": job_id,
            "status": job.get_status(),
            "message": "Job is being processed"
        }
    except Exception:
        return {
            "job_id": job_id,
            "status": submission.status,
            "message": "Job status unknown"
        }


# ==================== ADMIN ENDPOINTS ====================

@app.get("/api/admin/summary")
def admin_summary(db: Session = Depends(get_db)):
    """Get summary statistics for admin panel"""
    return submission_service.get_statistics(db)


@app.get("/api/admin/submissions")
def admin_submissions(
    limit: int = 50,
    offset: int = 0,
    problem_id: Optional[str] = None,
    student_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get recent submissions with filters"""
    return submission_service.list_submissions(
        db=db,
        limit=limit,
        offset=offset,
        problem_id=problem_id,
        student_id=student_id
    )


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "api"}
