"""
FastAPI application with RQ job queue integration
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from redis import Redis
from rq import Queue
from rq.job import Job
import pathlib
import json

from .database import get_db, init_db, SessionLocal
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
def get_result(job_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
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
        job_status = job.get_status()
        return {
            "job_id": job_id,
            "status": job_status,
            "message": "Job is being processed"
        }
    except Exception as e:
        logger.warning(
            f"Could not fetch RQ job {job_id}: {e}",
            extra={"job_id": job_id, "submission_id": submission.id}
        )
        return {
            "job_id": job_id,
            "status": submission.status,
            "message": "Job status unknown - check database record"
        }


# ==================== ADMIN ENDPOINTS ====================

@app.get("/api/admin/summary")
def admin_summary(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get summary statistics for admin panel"""
    return submission_service.get_statistics(db)


@app.get("/api/admin/submissions")
def admin_submissions(
    limit: int = 50,
    offset: int = 0,
    problem_id: Optional[str] = None,
    student_id: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get recent submissions with filters"""
    return submission_service.list_submissions(
        db=db,
        limit=limit,
        offset=offset,
        problem_id=problem_id,
        student_id=student_id
    )


@app.get("/api/subjects")
def list_subjects() -> Dict[str, Any]:
    """Get list of all subjects (materias)"""
    from .services.subject_service import subject_service
    logger.info("Fetching list of subjects")
    return {"subjects": subject_service.list_all_subjects()}


@app.get("/api/subjects/{subject_id}")
def get_subject(subject_id: str) -> Dict[str, Any]:
    """Get a specific subject with its units"""
    from .services.subject_service import subject_service
    logger.info(f"Fetching subject: {subject_id}")

    subject = subject_service.get_subject(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject '{subject_id}' not found")

    return subject


@app.get("/api/subjects/{subject_id}/units")
def list_units(subject_id: str) -> Dict[str, Any]:
    """Get all units for a specific subject"""
    from .services.subject_service import subject_service
    logger.info(f"Fetching units for subject: {subject_id}")

    units = subject_service.list_units_by_subject(subject_id)
    if not units:
        # Check if subject exists
        subject = subject_service.get_subject(subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail=f"Subject '{subject_id}' not found")

    return {"subject_id": subject_id, "units": units}


@app.get("/api/subjects/{subject_id}/units/{unit_id}/problems")
def list_problems_by_unit(subject_id: str, unit_id: str) -> Dict[str, Any]:
    """Get all problems for a specific unit"""
    from .services.subject_service import subject_service

    logger.info(f"Fetching problems for {subject_id}/{unit_id}")

    # Validate subject and unit exist
    if not subject_service.validate_subject_unit(subject_id, unit_id):
        raise HTTPException(
            status_code=404,
            detail=f"Unit '{unit_id}' not found in subject '{subject_id}'"
        )

    # Get filtered problems
    problems = problem_service.list_by_subject_and_unit(
        subject_id=subject_id,
        unit_id=unit_id
    )

    return {
        "subject_id": subject_id,
        "unit_id": unit_id,
        "problems": problems,
        "count": len(problems)
    }


@app.get("/api/problems/hierarchy")
def get_problems_hierarchy() -> Dict[str, Any]:
    """Get complete hierarchy: subjects -> units -> problems"""
    from .services.subject_service import subject_service

    logger.info("Fetching complete problems hierarchy")

    # Get subjects and units
    hierarchy = subject_service.get_hierarchy()

    # Get problems grouped by subject and unit
    problems_grouped = problem_service.group_by_subject_and_unit()

    # Merge problems into hierarchy
    for subject_id in hierarchy:
        for unit_id in hierarchy[subject_id].get("units", {}):
            # Add problem count
            problem_ids = problems_grouped.get(subject_id, {}).get(unit_id, [])
            hierarchy[subject_id]["units"][unit_id]["problem_count"] = len(problem_ids)
            hierarchy[subject_id]["units"][unit_id]["problem_ids"] = problem_ids

    return {"hierarchy": hierarchy}


@app.get("/api/health")
def health_check() -> Dict[str, Any]:
    """Health check endpoint with dependency checks"""
    from datetime import datetime
    from fastapi.responses import JSONResponse

    checks = {
        "service": "api",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "healthy"
    }

    # Check database
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"
        checks["status"] = "degraded"
        logger.error("Health check: Database unhealthy", exc_info=True)

    # Check Redis
    try:
        redis_conn.ping()
        checks["redis"] = "healthy"
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)}"
        checks["status"] = "degraded"
        logger.error("Health check: Redis unhealthy", exc_info=True)

    # Check queue
    try:
        queue_length = len(queue)
        checks["queue_length"] = str(queue_length)
        checks["queue"] = "healthy"
    except Exception as e:
        checks["queue"] = f"unhealthy: {str(e)}"
        checks["status"] = "degraded"
        logger.error("Health check: Queue unhealthy", exc_info=True)

    # Check problems directory
    try:
        problems = problem_service.list_all()
        problem_count = len(problems)
        checks["problems_count"] = str(problem_count)
        checks["problems"] = "healthy" if problem_count > 0 else "warning: no problems loaded"
    except Exception as e:
        checks["problems"] = f"unhealthy: {str(e)}"
        checks["status"] = "degraded"
        logger.error("Health check: Problems unhealthy", exc_info=True)

    # Return 503 if unhealthy, 200 if healthy
    status_code = 200 if checks["status"] == "healthy" else 503

    return JSONResponse(content=checks, status_code=status_code)
