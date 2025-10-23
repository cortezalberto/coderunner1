"""
Submission management service
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import Submission, TestResult
from ..exceptions import ValidationError
from ..logging_config import get_logger

logger = get_logger(__name__)


class SubmissionService:
    """Service for managing submissions"""

    def create_submission(
        self,
        db: Session,
        problem_id: str,
        code: str,
        student_id: Optional[str] = None
    ) -> Submission:
        """Create a new submission in pending state"""
        submission = Submission(
            job_id="",  # Will be assigned after enqueueing
            student_id=student_id,
            problem_id=problem_id,
            code=code,
            status="pending"
        )
        db.add(submission)
        db.commit()
        db.refresh(submission)

        logger.info(
            f"Created submission {submission.id}",
            extra={"submission_id": submission.id, "problem_id": problem_id}
        )
        return submission

    def update_job_id(self, db: Session, submission_id: int, job_id: str) -> Submission:
        """Update submission with job_id and set status to queued"""
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            raise ValidationError(f"Submission {submission_id} not found")

        submission.job_id = job_id
        submission.status = "queued"
        db.commit()
        db.refresh(submission)

        logger.info(
            f"Updated submission {submission_id} with job_id {job_id}",
            extra={"submission_id": submission_id, "job_id": job_id}
        )
        return submission

    def get_by_job_id(self, db: Session, job_id: str) -> Optional[Submission]:
        """Get submission by job_id"""
        return db.query(Submission).filter(Submission.job_id == job_id).first()

    def get_by_id(self, db: Session, submission_id: int) -> Optional[Submission]:
        """Get submission by id"""
        return db.query(Submission).filter(Submission.id == submission_id).first()

    def get_result_dict(self, submission: Submission) -> Dict[str, Any]:
        """Convert submission to result dictionary with test results"""
        test_results = []
        for tr in submission.test_results:
            test_results.append({
                "test_name": tr.test_name,
                "outcome": tr.outcome,
                "duration": tr.duration,
                "message": tr.message,
                "points": tr.points,
                "max_points": tr.max_points,
                "visibility": tr.visibility
            })

        return {
            "job_id": submission.job_id,
            "status": submission.status,
            "ok": submission.ok,
            "score_total": submission.score_total,
            "score_max": submission.score_max,
            "passed": submission.passed,
            "failed": submission.failed,
            "errors": submission.errors,
            "duration_sec": submission.duration_sec,
            "stdout": submission.stdout,
            "stderr": submission.stderr,
            "error_message": submission.error_message,
            "test_results": test_results,
            "created_at": submission.created_at.isoformat(),
            "completed_at": submission.completed_at.isoformat() if submission.completed_at else None
        }

    def get_statistics(self, db: Session) -> Dict[str, Any]:
        """Get aggregate statistics for admin panel"""
        total_submissions = db.query(Submission).count()
        completed = db.query(Submission).filter(Submission.status == "completed").count()
        failed = db.query(Submission).filter(Submission.status == "failed").count()
        pending = db.query(Submission).filter(
            Submission.status.in_(["pending", "queued", "running"])
        ).count()

        # Average score
        avg_score = db.query(func.avg(Submission.score_total)).filter(
            Submission.status == "completed"
        ).scalar() or 0.0

        # Statistics by problem
        by_problem = db.query(
            Submission.problem_id,
            func.count(Submission.id).label("count"),
            func.avg(Submission.score_total).label("avg_score")
        ).filter(
            Submission.status == "completed"
        ).group_by(Submission.problem_id).all()

        problems_stats = [
            {
                "problem_id": p.problem_id,
                "submissions": p.count,
                "avg_score": round(float(p.avg_score or 0), 2)
            }
            for p in by_problem
        ]

        logger.info(
            f"Generated statistics: {total_submissions} total submissions",
            extra={"total": total_submissions, "completed": completed}
        )

        return {
            "total_submissions": total_submissions,
            "completed": completed,
            "failed": failed,
            "pending": pending,
            "avg_score": round(float(avg_score), 2),
            "by_problem": problems_stats
        }

    def list_submissions(
        self,
        db: Session,
        limit: int = 50,
        offset: int = 0,
        problem_id: Optional[str] = None,
        student_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get recent submissions with filters"""
        query = db.query(Submission)

        if problem_id:
            query = query.filter(Submission.problem_id == problem_id)
        if student_id:
            query = query.filter(Submission.student_id == student_id)

        total = query.count()
        submissions = query.order_by(Submission.created_at.desc()).offset(offset).limit(limit).all()

        results = []
        for sub in submissions:
            results.append({
                "id": sub.id,
                "job_id": sub.job_id,
                "student_id": sub.student_id,
                "problem_id": sub.problem_id,
                "status": sub.status,
                "ok": sub.ok,
                "score_total": sub.score_total,
                "score_max": sub.score_max,
                "passed": sub.passed,
                "failed": sub.failed,
                "errors": sub.errors,
                "duration_sec": sub.duration_sec,
                "created_at": sub.created_at.isoformat(),
                "completed_at": sub.completed_at.isoformat() if sub.completed_at else None
            })

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "submissions": results
        }


# Singleton instance
submission_service = SubmissionService()
