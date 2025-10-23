"""
Tests for SubmissionService
"""
import pytest
from datetime import datetime
from backend.services.submission_service import SubmissionService
from backend.models import Submission, TestResult


class TestSubmissionService:
    """Test cases for SubmissionService"""

    def test_create_submission(self, test_db, sample_submission_data):
        """Test creating a new submission"""
        service = SubmissionService()

        submission = service.create_submission(
            db=test_db,
            problem_id=sample_submission_data["problem_id"],
            code=sample_submission_data["code"],
            student_id=sample_submission_data["student_id"]
        )

        assert submission.id is not None
        assert submission.problem_id == "sumatoria"
        assert submission.code == sample_submission_data["code"]
        assert submission.student_id == "student-001"
        assert submission.status == "pending"
        assert submission.created_at is not None

    def test_create_submission_without_student_id(self, test_db, sample_submission_data):
        """Test creating submission without student_id"""
        service = SubmissionService()

        submission = service.create_submission(
            db=test_db,
            problem_id=sample_submission_data["problem_id"],
            code=sample_submission_data["code"],
            student_id=None
        )

        assert submission.student_id is None
        assert submission.problem_id == "sumatoria"

    def test_update_job_id(self, test_db, sample_submission_data):
        """Test updating submission with job_id"""
        service = SubmissionService()

        # Create submission
        submission = service.create_submission(
            db=test_db,
            problem_id=sample_submission_data["problem_id"],
            code=sample_submission_data["code"]
        )

        # Update with job_id
        service.update_job_id(test_db, submission.id, "job-abc-123")
        test_db.refresh(submission)

        assert submission.job_id == "job-abc-123"
        assert submission.status == "queued"

    def test_get_by_job_id_exists(self, test_db, sample_submission_data):
        """Test getting submission by job_id when it exists"""
        service = SubmissionService()

        # Create and update submission
        submission = service.create_submission(
            db=test_db,
            problem_id=sample_submission_data["problem_id"],
            code=sample_submission_data["code"]
        )
        service.update_job_id(test_db, submission.id, "job-test-123")

        # Retrieve by job_id
        found = service.get_by_job_id(test_db, "job-test-123")

        assert found is not None
        assert found.id == submission.id
        assert found.job_id == "job-test-123"

    def test_get_by_job_id_not_exists(self, test_db):
        """Test getting submission by non-existent job_id"""
        service = SubmissionService()

        found = service.get_by_job_id(test_db, "nonexistent-job")

        assert found is None

    def test_get_by_id_exists(self, test_db, sample_submission_data):
        """Test getting submission by id when it exists"""
        service = SubmissionService()

        submission = service.create_submission(
            db=test_db,
            problem_id=sample_submission_data["problem_id"],
            code=sample_submission_data["code"]
        )

        found = service.get_by_id(test_db, submission.id)

        assert found is not None
        assert found.id == submission.id

    def test_get_by_id_not_exists(self, test_db):
        """Test getting submission by non-existent id"""
        service = SubmissionService()

        found = service.get_by_id(test_db, 99999)

        assert found is None

    def test_get_result_dict_with_test_results(self, test_db, sample_submission_data, sample_test_result_data):
        """Test converting submission to dict with test results"""
        service = SubmissionService()

        # Create submission
        submission = service.create_submission(
            db=test_db,
            problem_id=sample_submission_data["problem_id"],
            code=sample_submission_data["code"]
        )
        submission.job_id = "job-123"
        submission.status = "completed"
        submission.ok = True
        submission.score_total = 3.0
        submission.score_max = 10.0
        submission.passed = 1
        submission.failed = 0
        submission.errors = 0
        test_db.commit()

        # Add test result
        test_result = TestResult(
            submission_id=submission.id,
            **sample_test_result_data
        )
        test_db.add(test_result)
        test_db.commit()
        test_db.refresh(submission)

        # Get result dict
        result = service.get_result_dict(submission)

        assert result["job_id"] == "job-123"
        assert result["status"] == "completed"
        assert result["ok"] is True
        assert result["score_total"] == 3.0
        assert result["score_max"] == 10.0
        assert result["passed"] == 1
        assert len(result["test_results"]) == 1
        assert result["test_results"][0]["test_name"] == "test_suma_basico"
        assert result["test_results"][0]["outcome"] == "passed"

    def test_get_result_dict_without_test_results(self, test_db, sample_submission_data):
        """Test converting submission to dict without test results"""
        service = SubmissionService()

        submission = service.create_submission(
            db=test_db,
            problem_id=sample_submission_data["problem_id"],
            code=sample_submission_data["code"]
        )
        submission.job_id = "job-456"
        submission.status = "queued"
        test_db.commit()

        result = service.get_result_dict(submission)

        assert result["job_id"] == "job-456"
        assert result["status"] == "queued"
        assert result["test_results"] == []

    def test_get_statistics_empty_database(self, test_db):
        """Test statistics with no submissions"""
        service = SubmissionService()

        stats = service.get_statistics(test_db)

        assert stats["total_submissions"] == 0
        assert stats["completed"] == 0
        assert stats["failed"] == 0
        assert stats["pending"] == 0
        assert stats["avg_score"] == 0.0
        assert stats["by_problem"] == []

    def test_get_statistics_with_submissions(self, test_db, sample_submission_data):
        """Test statistics with multiple submissions"""
        service = SubmissionService()

        # Create completed submission
        sub1 = service.create_submission(
            db=test_db,
            problem_id="sumatoria",
            code=sample_submission_data["code"]
        )
        sub1.status = "completed"
        sub1.ok = True
        sub1.score_total = 8.0
        sub1.score_max = 10.0

        # Create failed submission
        sub2 = service.create_submission(
            db=test_db,
            problem_id="sumatoria",
            code="bad code"
        )
        sub2.status = "failed"
        sub2.ok = False

        # Create pending submission
        sub3 = service.create_submission(
            db=test_db,
            problem_id="otro_problema",
            code=sample_submission_data["code"]
        )

        test_db.commit()

        stats = service.get_statistics(test_db)

        assert stats["total_submissions"] == 3
        assert stats["completed"] == 1
        assert stats["failed"] == 1
        assert stats["pending"] == 1
        assert stats["avg_score"] == 8.0  # Only completed submissions count
        assert len(stats["by_problem"]) == 2

    def test_list_submissions_no_filters(self, test_db, sample_submission_data):
        """Test listing submissions without filters"""
        service = SubmissionService()

        # Create multiple submissions
        for i in range(5):
            service.create_submission(
                db=test_db,
                problem_id="sumatoria",
                code=sample_submission_data["code"],
                student_id=f"student-{i}"
            )
        test_db.commit()

        submissions = service.list_submissions(test_db, limit=10, offset=0)

        assert len(submissions) == 5

    def test_list_submissions_with_limit_offset(self, test_db, sample_submission_data):
        """Test pagination with limit and offset"""
        service = SubmissionService()

        # Create 10 submissions
        for i in range(10):
            service.create_submission(
                db=test_db,
                problem_id="sumatoria",
                code=sample_submission_data["code"]
            )
        test_db.commit()

        # Get first page
        page1 = service.list_submissions(test_db, limit=3, offset=0)
        assert len(page1) == 3

        # Get second page
        page2 = service.list_submissions(test_db, limit=3, offset=3)
        assert len(page2) == 3

        # Ensure different submissions
        assert page1[0].id != page2[0].id

    def test_list_submissions_filter_by_problem(self, test_db, sample_submission_data):
        """Test filtering submissions by problem_id"""
        service = SubmissionService()

        # Create submissions for different problems
        service.create_submission(db=test_db, problem_id="sumatoria", code="code1")
        service.create_submission(db=test_db, problem_id="sumatoria", code="code2")
        service.create_submission(db=test_db, problem_id="otro", code="code3")
        test_db.commit()

        submissions = service.list_submissions(test_db, problem_id="sumatoria")

        assert len(submissions) == 2
        assert all(s.problem_id == "sumatoria" for s in submissions)

    def test_list_submissions_filter_by_student(self, test_db, sample_submission_data):
        """Test filtering submissions by student_id"""
        service = SubmissionService()

        # Create submissions for different students
        service.create_submission(db=test_db, problem_id="sumatoria", code="code1", student_id="alice")
        service.create_submission(db=test_db, problem_id="sumatoria", code="code2", student_id="alice")
        service.create_submission(db=test_db, problem_id="sumatoria", code="code3", student_id="bob")
        test_db.commit()

        submissions = service.list_submissions(test_db, student_id="alice")

        assert len(submissions) == 2
        assert all(s.student_id == "alice" for s in submissions)

    def test_singleton_instance(self):
        """Test that submission_service is a singleton"""
        from backend.services.submission_service import submission_service

        assert submission_service is not None
        assert isinstance(submission_service, SubmissionService)
