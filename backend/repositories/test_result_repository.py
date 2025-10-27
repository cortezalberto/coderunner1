"""
Test Result Repository

Data access layer for TestResult model.
"""
from typing import List
from sqlalchemy.orm import Session
from ..models import TestResult
from ..logging_config import get_logger

logger = get_logger(__name__)


class TestResultRepository:
    """Repository for TestResult data access"""

    def create_bulk(
        self,
        db: Session,
        test_results: List[TestResult]
    ) -> None:
        """
        Create multiple test results in bulk.

        Args:
            db: Database session
            test_results: List of TestResult objects

        Performance: Uses bulk insert for better performance.
        """
        db.bulk_save_objects(test_results)
        db.flush()

    def find_by_submission_id(
        self,
        db: Session,
        submission_id: int
    ) -> List[TestResult]:
        """
        Find all test results for a submission.

        Args:
            db: Database session
            submission_id: Submission ID

        Returns:
            List of TestResult objects
        """
        return db.query(TestResult).filter(
            TestResult.submission_id == submission_id
        ).all()


# Singleton instance
test_result_repository = TestResultRepository()
