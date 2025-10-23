"""
Tests for ProblemService
"""
import pytest
import json
from pathlib import Path
from backend.services.problem_service import ProblemService
from backend.exceptions import ProblemNotFoundError


class TestProblemService:
    """Test cases for ProblemService"""

    def test_list_all_problems(self, mock_problem_dir, monkeypatch):
        """Test listing all available problems"""
        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)
        problems = service.list_all()

        assert "sumatoria" in problems
        assert "metadata" in problems["sumatoria"]
        assert "prompt" in problems["sumatoria"]
        assert "starter" in problems["sumatoria"]

        # Check metadata structure
        metadata = problems["sumatoria"]["metadata"]
        assert metadata["title"] == "Suma Simple"
        assert metadata["difficulty"] == "easy"
        assert "basics" in metadata["tags"]
        assert metadata["timeout_sec"] == 3.0
        assert metadata["memory_mb"] == 128

    def test_get_problem_dir_exists(self, mock_problem_dir, monkeypatch):
        """Test getting directory for existing problem"""
        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)
        problem_dir = service.get_problem_dir("sumatoria")

        assert problem_dir.exists()
        assert problem_dir.is_dir()
        assert problem_dir.name == "sumatoria"

    def test_get_problem_dir_not_exists(self, mock_problem_dir, monkeypatch):
        """Test getting directory for non-existing problem"""
        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)

        with pytest.raises(ProblemNotFoundError) as exc_info:
            service.get_problem_dir("nonexistent")

        assert "not found" in str(exc_info.value).lower()

    def test_get_test_files_both_exist(self, mock_problem_dir, monkeypatch):
        """Test getting test files when both public and hidden exist"""
        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)
        problem_dir = mock_problem_dir / "sumatoria"

        tests_public, tests_hidden = service.get_test_files(problem_dir)

        assert tests_public.exists()
        assert tests_public.name == "tests_public.py"
        assert tests_hidden.exists()
        assert tests_hidden.name == "tests_hidden.py"

    def test_get_test_files_legacy_fallback(self, mock_problem_dir, monkeypatch):
        """Test fallback to tests.py when public/hidden don't exist"""
        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)
        problem_dir = mock_problem_dir / "sumatoria"

        # Remove public/hidden and create legacy tests.py
        (problem_dir / "tests_public.py").unlink()
        (problem_dir / "tests_hidden.py").unlink()
        (problem_dir / "tests.py").write_text("def test_legacy():\n    assert True")

        tests_public, tests_hidden = service.get_test_files(problem_dir)

        assert tests_public.exists()
        assert tests_public.name == "tests.py"
        assert tests_hidden is None

    def test_get_test_files_not_found(self, mock_problem_dir, monkeypatch):
        """Test error when no test files exist"""
        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)
        problem_dir = mock_problem_dir / "sumatoria"

        # Remove all test files
        (problem_dir / "tests_public.py").unlink()
        (problem_dir / "tests_hidden.py").unlink()

        with pytest.raises(ProblemNotFoundError) as exc_info:
            service.get_test_files(problem_dir)

        assert "test files" in str(exc_info.value).lower()

    def test_load_rubric_success(self, mock_problem_dir, monkeypatch):
        """Test loading rubric from problem directory"""
        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)
        problem_dir = mock_problem_dir / "sumatoria"

        rubric = service.load_rubric(problem_dir)

        assert "tests" in rubric
        assert "max_points" in rubric
        assert len(rubric["tests"]) == 3
        assert rubric["max_points"] == 10

        # Check first test entry
        first_test = rubric["tests"][0]
        assert first_test["name"] == "test_suma_basico"
        assert first_test["points"] == 3
        assert first_test["visibility"] == "public"

    def test_load_rubric_file_not_found(self, mock_problem_dir, monkeypatch):
        """Test error when rubric.json doesn't exist"""
        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)
        problem_dir = mock_problem_dir / "sumatoria"

        # Remove rubric.json
        (problem_dir / "rubric.json").unlink()

        with pytest.raises(ProblemNotFoundError) as exc_info:
            service.load_rubric(problem_dir)

        assert "rubric.json" in str(exc_info.value).lower()

    def test_load_rubric_invalid_json(self, mock_problem_dir, monkeypatch):
        """Test error when rubric.json has invalid JSON"""
        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)
        problem_dir = mock_problem_dir / "sumatoria"

        # Write invalid JSON
        (problem_dir / "rubric.json").write_text("{ invalid json }")

        with pytest.raises(Exception):  # Could be ValueError or JSONDecodeError
            service.load_rubric(problem_dir)

    def test_list_all_handles_missing_metadata(self, mock_problem_dir, monkeypatch):
        """Test list_all gracefully handles problems with missing metadata"""
        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)

        # Create a problem without metadata.json
        bad_problem = mock_problem_dir / "bad_problem"
        bad_problem.mkdir()

        problems = service.list_all()

        # Should still list sumatoria, but skip bad_problem
        assert "sumatoria" in problems
        # Bad problem might be included with error or excluded - either is acceptable

    def test_singleton_instance(self):
        """Test that problem_service is a singleton"""
        from backend.services.problem_service import problem_service

        assert problem_service is not None
        assert isinstance(problem_service, ProblemService)
