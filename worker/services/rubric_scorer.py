"""
Rubric Scorer Service - Applies scoring rubrics to test results
"""
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class TestScore:
    """Score for a single test"""
    test_name: str
    outcome: str
    duration: float
    message: str
    points: float
    max_points: float
    visibility: str


@dataclass
class ScoringResult:
    """Complete scoring result"""
    test_scores: List[TestScore]
    score_total: float
    score_max: float
    passed: int
    failed: int
    errors: int


class RubricScorer:
    """Service for scoring test results against rubrics"""

    def score(
        self,
        test_details: List[Dict[str, Any]],
        rubric: Dict[str, Any]
    ) -> ScoringResult:
        """
        Apply rubric to test results

        Args:
            test_details: List of test results from pytest
            rubric: Rubric definition with points per test

        Returns:
            ScoringResult with scores and statistics
        """
        # Build rubric map
        rubric_map = {t["name"]: t for t in rubric.get("tests", [])}

        # Score each test
        test_scores = []
        passed = failed = errors = 0
        score_total = 0.0
        score_max = rubric.get("max_points", 0)

        for test in test_details:
            # Extract test name (remove path prefix if present)
            test_name = test["name"].split("::")[-1]
            outcome = test["outcome"]

            # Count outcomes
            if outcome == "passed":
                passed += 1
            elif outcome == "failed":
                failed += 1
            else:
                errors += 1

            # Get rubric entry
            rubric_entry = rubric_map.get(test_name, {})
            max_points = rubric_entry.get("points", 0)
            points = max_points if outcome == "passed" else 0
            visibility = rubric_entry.get("visibility", "public")

            # Add to total score
            score_total += points

            # Create test score
            test_score = TestScore(
                test_name=test_name,
                outcome=outcome,
                duration=test["duration"],
                message=test["message"][:500],  # Limit message size
                points=points,
                max_points=max_points,
                visibility=visibility
            )
            test_scores.append(test_score)

        return ScoringResult(
            test_scores=test_scores,
            score_total=score_total,
            score_max=score_max,
            passed=passed,
            failed=failed,
            errors=errors
        )


# Singleton instance
rubric_scorer = RubricScorer()
