"""
Tests for RubricScorer service
"""
import pytest
from worker.services.rubric_scorer import RubricScorer, TestScore, ScoringResult


class TestRubricScorer:
    """Test cases for RubricScorer"""

    def test_extract_test_name_simple(self):
        """Test extracting simple test name"""
        scorer = RubricScorer()

        assert scorer._extract_test_name("test_suma_basico") == "test_suma_basico"
        assert scorer._extract_test_name("test_suma") == "test_suma"

    def test_extract_test_name_with_path(self):
        """Test extracting test name from full path"""
        scorer = RubricScorer()

        nodeid = "tests_public.py::test_suma_basico"
        assert scorer._extract_test_name(nodeid) == "test_suma_basico"

        nodeid = "tests_hidden.py::TestSuma::test_suma_negativos"
        assert scorer._extract_test_name(nodeid) == "test_suma_negativos"

    def test_extract_test_name_with_parameters(self):
        """Test extracting test name with parameters"""
        scorer = RubricScorer()

        nodeid = "tests_public.py::test_suma_basico[1-2-3]"
        assert scorer._extract_test_name(nodeid) == "test_suma_basico"

    def test_score_all_passed(self, sample_rubric):
        """Test scoring when all tests pass"""
        scorer = RubricScorer()

        test_details = [
            {
                "nodeid": "tests_public.py::test_suma_basico",
                "outcome": "passed",
                "duration": 0.001,
                "longrepr": ""
            },
            {
                "nodeid": "tests_public.py::test_suma_negativos",
                "outcome": "passed",
                "duration": 0.002,
                "longrepr": ""
            },
            {
                "nodeid": "tests_hidden.py::test_suma_grande",
                "outcome": "passed",
                "duration": 0.003,
                "longrepr": ""
            }
        ]

        result = scorer.score(test_details, sample_rubric)

        assert isinstance(result, ScoringResult)
        assert result.score_total == 10.0
        assert result.score_max == 10.0
        assert result.passed == 3
        assert result.failed == 0
        assert result.errors == 0
        assert len(result.test_scores) == 3

    def test_score_some_failed(self, sample_rubric):
        """Test scoring when some tests fail"""
        scorer = RubricScorer()

        test_details = [
            {
                "nodeid": "tests_public.py::test_suma_basico",
                "outcome": "passed",
                "duration": 0.001,
                "longrepr": ""
            },
            {
                "nodeid": "tests_public.py::test_suma_negativos",
                "outcome": "failed",
                "duration": 0.002,
                "longrepr": "AssertionError: Expected 1, got 2"
            },
            {
                "nodeid": "tests_hidden.py::test_suma_grande",
                "outcome": "passed",
                "duration": 0.003,
                "longrepr": ""
            }
        ]

        result = scorer.score(test_details, sample_rubric)

        assert result.score_total == 8.0  # 3 (basico) + 0 (negativos) + 5 (grande)
        assert result.score_max == 10.0
        assert result.passed == 2
        assert result.failed == 1
        assert result.errors == 0

    def test_score_with_errors(self, sample_rubric):
        """Test scoring when tests have errors"""
        scorer = RubricScorer()

        test_details = [
            {
                "nodeid": "tests_public.py::test_suma_basico",
                "outcome": "passed",
                "duration": 0.001,
                "longrepr": ""
            },
            {
                "nodeid": "tests_public.py::test_suma_negativos",
                "outcome": "error",
                "duration": 0.0,
                "longrepr": "ImportError: No module named 'student_code'"
            },
            {
                "nodeid": "tests_hidden.py::test_suma_grande",
                "outcome": "passed",
                "duration": 0.003,
                "longrepr": ""
            }
        ]

        result = scorer.score(test_details, sample_rubric)

        assert result.score_total == 8.0  # 3 + 0 (error) + 5
        assert result.passed == 2
        assert result.failed == 0
        assert result.errors == 1

    def test_score_visibility_public(self, sample_rubric):
        """Test that public tests have correct visibility"""
        scorer = RubricScorer()

        test_details = [
            {
                "nodeid": "tests_public.py::test_suma_basico",
                "outcome": "passed",
                "duration": 0.001,
                "longrepr": ""
            }
        ]

        result = scorer.score(test_details, sample_rubric)

        test_score = result.test_scores[0]
        assert test_score.visibility == "public"

    def test_score_visibility_hidden(self, sample_rubric):
        """Test that hidden tests have correct visibility"""
        scorer = RubricScorer()

        test_details = [
            {
                "nodeid": "tests_hidden.py::test_suma_grande",
                "outcome": "passed",
                "duration": 0.003,
                "longrepr": ""
            }
        ]

        result = scorer.score(test_details, sample_rubric)

        test_score = result.test_scores[0]
        assert test_score.visibility == "hidden"

    def test_score_test_not_in_rubric(self):
        """Test scoring when test is not defined in rubric"""
        scorer = RubricScorer()

        test_details = [
            {
                "nodeid": "tests_public.py::test_unknown",
                "outcome": "passed",
                "duration": 0.001,
                "longrepr": ""
            }
        ]

        rubric = {
            "tests": [
                {"name": "test_suma_basico", "points": 3, "visibility": "public"}
            ],
            "max_points": 3
        }

        result = scorer.score(test_details, rubric)

        # Unknown test should have 0 points and unknown visibility
        assert len(result.test_scores) == 1
        test_score = result.test_scores[0]
        assert test_score.points == 0.0
        assert test_score.max_points == 0.0
        assert test_score.visibility == "unknown"

    def test_score_empty_test_details(self, sample_rubric):
        """Test scoring with no test results"""
        scorer = RubricScorer()

        result = scorer.score([], sample_rubric)

        assert result.score_total == 0.0
        assert result.score_max == 10.0
        assert result.passed == 0
        assert result.failed == 0
        assert result.errors == 0
        assert len(result.test_scores) == 0

    def test_score_message_preserved(self, sample_rubric):
        """Test that error messages are preserved"""
        scorer = RubricScorer()

        error_message = "AssertionError: Expected 5, got 3"
        test_details = [
            {
                "nodeid": "tests_public.py::test_suma_basico",
                "outcome": "failed",
                "duration": 0.001,
                "longrepr": error_message
            }
        ]

        result = scorer.score(test_details, sample_rubric)

        test_score = result.test_scores[0]
        assert test_score.message == error_message

    def test_score_duration_preserved(self, sample_rubric):
        """Test that test duration is preserved"""
        scorer = RubricScorer()

        test_details = [
            {
                "nodeid": "tests_public.py::test_suma_basico",
                "outcome": "passed",
                "duration": 1.234,
                "longrepr": ""
            }
        ]

        result = scorer.score(test_details, sample_rubric)

        test_score = result.test_scores[0]
        assert test_score.duration == 1.234

    def test_score_skipped_tests(self, sample_rubric):
        """Test scoring with skipped tests"""
        scorer = RubricScorer()

        test_details = [
            {
                "nodeid": "tests_public.py::test_suma_basico",
                "outcome": "skipped",
                "duration": 0.0,
                "longrepr": "Skipped: reason"
            }
        ]

        result = scorer.score(test_details, sample_rubric)

        # Skipped tests count as errors
        assert result.errors == 1
        assert result.passed == 0
        assert result.failed == 0

    def test_singleton_instance(self):
        """Test that rubric_scorer is a singleton"""
        from worker.services.rubric_scorer import rubric_scorer

        assert rubric_scorer is not None
        assert isinstance(rubric_scorer, RubricScorer)

    def test_scoring_result_dataclass(self):
        """Test ScoringResult dataclass structure"""
        test_scores = [
            TestScore(
                test_name="test_1",
                outcome="passed",
                duration=0.1,
                message="",
                points=5.0,
                max_points=5.0,
                visibility="public"
            )
        ]

        result = ScoringResult(
            test_scores=test_scores,
            score_total=5.0,
            score_max=10.0,
            passed=1,
            failed=0,
            errors=0
        )

        assert result.test_scores == test_scores
        assert result.score_total == 5.0
        assert result.score_max == 10.0
        assert result.passed == 1
        assert result.failed == 0
        assert result.errors == 0
