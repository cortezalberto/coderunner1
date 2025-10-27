"""
FastAPI application with RQ job queue integration

PERFORMANCE: Rate limiting configured for 300 concurrent users
- /api/submit: 5 req/min per IP (prevent spam submissions)
- /api/result/{job_id}: 30 req/min per IP (polling)
- /api/problems: 20 req/min per IP (reduce cache misses)
- Admin endpoints: 60 req/min per IP (higher limit for teachers)
"""
from fastapi import FastAPI, Depends, HTTPException, Request
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
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .database import get_db, init_db, SessionLocal, engine
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

# Rate limiting configuration
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI(title="Python Playground Suite")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection pool for RQ (DB 0)
# PERFORMANCE: Connection pooling for 300 concurrent users
# - max_connections=50: Matches backend pool (20 + 30 overflow)
# - socket_keepalive=True: Prevent stale connections
# - socket_timeout=5: Fail fast on network issues
# - retry_on_timeout=True: Auto-retry on temporary failures
from redis.connection import ConnectionPool

redis_pool = ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    max_connections=50,
    socket_keepalive=True,
    socket_timeout=5,
    retry_on_timeout=True,
    decode_responses=False
)
redis_conn = Redis(connection_pool=redis_pool)
queue = Queue("submissions", connection=redis_conn)


@app.on_event("startup")
def startup_event():
    """Initialize database and logging on startup"""
    setup_logging()
    logger.info("Starting Python Playground API", extra={"version": "2.0.0"})
    init_db()
    logger.info("Database initialized successfully")


@app.get("/api/problems")
@limiter.limit("20/minute")
async def list_problems(request: Request) -> Dict[str, Any]:
    """List all available problems with metadata and prompts

    Rate limit: 20 requests per minute per IP
    ASYNC: Non-blocking for better concurrency under load
    """
    logger.info("Fetching list of problems")
    return problem_service.list_all()


@app.post("/api/submit", response_model=SubmissionResponse)
@limiter.limit("5/minute")
async def submit(request: Request, req: SubmissionRequest, db: Session = Depends(get_db)):
    """Submit code for evaluation - enqueues job

    Rate limit: 5 requests per minute per IP (prevents spam submissions)
    ASYNC: Non-blocking for high throughput under concurrent load

    IMPROVEMENT: Atomic transaction - create submission + enqueue + update job_id
    in single transaction. Prevents race conditions and orphaned records.
    """
    logger.info(f"Received submission for problem: {req.problem_id}")

    # Validate request
    validate_submission_request(req)

    try:
        # Create submission in pending state (no commit yet)
        submission = Submission(
            job_id="",  # Will be assigned after enqueueing
            student_id=req.student_id,
            problem_id=req.problem_id,
            code=req.code,
            status="pending"
        )
        db.add(submission)
        db.flush()  # Get submission.id without committing

        logger.info(
            f"Created submission {submission.id} (pending commit)",
            extra={"submission_id": submission.id, "problem_id": req.problem_id}
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
        submission.job_id = job.id
        submission.status = "queued"

        # Atomic commit: submission + job_id update
        db.commit()
        db.refresh(submission)

        logger.info(
            f"Submission {submission.id} atomically committed with job_id {job.id}",
            extra={"submission_id": submission.id, "job_id": job.id}
        )

        return SubmissionResponse(
            job_id=job.id,
            status="queued",
            message="Submission enqueued successfully"
        )

    except Exception as e:
        # Rollback on any error
        db.rollback()
        logger.error(
            f"Failed to submit code: {e}",
            extra={"problem_id": req.problem_id, "error": str(e)},
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit code: {str(e)}"
        )


@app.get("/api/result/{job_id}")
@limiter.limit("30/minute")
async def get_result(request: Request, job_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get result of a submission by job_id

    Rate limit: 30 requests per minute per IP (supports exponential backoff polling)
    ASYNC: Non-blocking for concurrent polling from 300 users
    """
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
@limiter.limit("60/minute")
async def admin_summary(request: Request, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get summary statistics for admin panel

    Rate limit: 60 requests per minute per IP (higher limit for teachers)
    ASYNC: Non-blocking for dashboard real-time updates
    """
    return submission_service.get_statistics(db)


@app.get("/api/admin/submissions")
@limiter.limit("60/minute")
async def admin_submissions(
    request: Request,
    limit: int = 50,
    offset: int = 0,
    problem_id: Optional[str] = None,
    student_id: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get recent submissions with filters

    Rate limit: 60 requests per minute per IP (higher limit for teachers)
    ASYNC: Non-blocking for admin dashboard
    """
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
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint with dependency checks and performance metrics.

    PERFORMANCE: Monitors system health for 300 concurrent users.
    Returns metrics on database pool, Redis cache, queue length, etc.
    """
    from datetime import datetime
    from fastapi.responses import JSONResponse
    from .cache import get_cache_stats

    checks = {
        "service": "api",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "healthy",
        "metrics": {}
    }

    # Check database with connection pool metrics
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        checks["database"] = "healthy"

        # Get connection pool metrics
        pool = engine.pool
        checks["metrics"]["db_pool"] = {
            "size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "total_connections": pool.size() + pool.overflow()
        }
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"
        checks["status"] = "degraded"
        logger.error("Health check: Database unhealthy", exc_info=True)

    # Check Redis with cache statistics
    try:
        redis_conn.ping()
        checks["redis"] = "healthy"

        # Get cache statistics
        cache_stats = get_cache_stats()
        checks["metrics"]["cache"] = cache_stats
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)}"
        checks["status"] = "degraded"
        logger.error("Health check: Redis unhealthy", exc_info=True)

    # Check queue with metrics
    try:
        queue_length = len(queue)
        checks["queue_length"] = str(queue_length)
        checks["queue"] = "healthy"

        # Get queue metrics
        checks["metrics"]["queue"] = {
            "submissions_queue_length": queue_length,
            "worker_count": redis_conn.scard("rq:workers") if redis_conn else 0
        }
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

        # Add problems metrics
        checks["metrics"]["problems"] = {
            "total_count": problem_count,
            "cached": "yes" if redis_conn else "no"
        }
    except Exception as e:
        checks["problems"] = f"unhealthy: {str(e)}"
        checks["status"] = "degraded"
        logger.error("Health check: Problems unhealthy", exc_info=True)

    # Add system load metrics
    try:
        from sqlalchemy import text as sql_text
        db = SessionLocal()

        # Get total submissions processed
        total_submissions = db.execute(sql_text("SELECT COUNT(*) FROM submissions")).scalar()
        completed_today = db.execute(
            sql_text("SELECT COUNT(*) FROM submissions WHERE DATE(created_at) = CURRENT_DATE")
        ).scalar()

        db.close()

        checks["metrics"]["usage"] = {
            "total_submissions": total_submissions,
            "submissions_today": completed_today
        }
    except Exception as e:
        logger.warning(f"Could not get usage metrics: {e}")

    # Return 503 if unhealthy, 200 if healthy
    status_code = 200 if checks["status"] == "healthy" else 503

    return JSONResponse(content=checks, status_code=status_code)
