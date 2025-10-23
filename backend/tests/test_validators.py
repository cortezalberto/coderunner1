"""
Tests for validators
"""
import pytest
from backend.validators import (
    validate_code_length,
    validate_code_safety,
    validate_problem_exists,
    validate_problem_id_format,
    validate_submission_request
)
from backend.exceptions import ValidationError, ProblemNotFoundError


class TestValidateCodeLength:
    """Test cases for code length validation"""

    def test_valid_code_length(self):
        """Test code within length limit"""
        code = "def suma(a, b):\n    return a + b"
        # Should not raise
        validate_code_length(code, max_length=100)

    def test_code_too_long(self):
        """Test code exceeding length limit"""
        code = "x" * 1001

        with pytest.raises(ValidationError) as exc_info:
            validate_code_length(code, max_length=1000)

        assert "exceeds maximum length" in str(exc_info.value)
        assert "1001" in str(exc_info.value)
        assert "1000" in str(exc_info.value)

    def test_empty_code(self):
        """Test empty code string"""
        code = ""
        # Should not raise - empty is valid (will be caught by other validators)
        validate_code_length(code)

    def test_code_exactly_at_limit(self):
        """Test code exactly at the limit"""
        code = "x" * 1000
        # Should not raise
        validate_code_length(code, max_length=1000)


class TestValidateCodeSafety:
    """Test cases for code safety validation"""

    def test_safe_code(self):
        """Test code without dangerous imports"""
        code = "def suma(a, b):\n    return a + b"
        # Should not raise
        validate_code_safety(code)

    def test_dangerous_import_os(self):
        """Test code with os import"""
        code = "import os\nos.system('ls')"

        with pytest.raises(ValidationError) as exc_info:
            validate_code_safety(code)

        assert "dangerous import" in str(exc_info.value).lower()
        assert "os" in str(exc_info.value)

    def test_dangerous_import_subprocess(self):
        """Test code with subprocess import"""
        code = "import subprocess\nsubprocess.run(['ls'])"

        with pytest.raises(ValidationError) as exc_info:
            validate_code_safety(code)

        assert "subprocess" in str(exc_info.value)

    def test_dangerous_import_sys(self):
        """Test code with sys import"""
        code = "import sys\nsys.exit()"

        with pytest.raises(ValidationError) as exc_info:
            validate_code_safety(code)

        assert "sys" in str(exc_info.value)

    def test_dangerous_from_import(self):
        """Test code with from ... import"""
        code = "from os import system\nsystem('ls')"

        with pytest.raises(ValidationError) as exc_info:
            validate_code_safety(code)

        assert "os" in str(exc_info.value)

    def test_safe_imports(self):
        """Test code with safe imports"""
        code = """
import math
import json
from typing import List

def calculate(x):
    return math.sqrt(x)
"""
        # Should not raise
        validate_code_safety(code)

    def test_dangerous_eval(self):
        """Test code with eval"""
        code = "result = eval('2 + 2')"

        with pytest.raises(ValidationError) as exc_info:
            validate_code_safety(code)

        assert "eval" in str(exc_info.value).lower()

    def test_dangerous_exec(self):
        """Test code with exec"""
        code = "exec('print(hello)')"

        with pytest.raises(ValidationError) as exc_info:
            validate_code_safety(code)

        assert "exec" in str(exc_info.value).lower()

    def test_dangerous_open(self):
        """Test code with open"""
        code = "with open('/etc/passwd') as f:\n    data = f.read()"

        with pytest.raises(ValidationError) as exc_info:
            validate_code_safety(code)

        assert "open" in str(exc_info.value).lower()


class TestValidateProblemIdFormat:
    """Test cases for problem ID format validation"""

    def test_valid_alphanumeric(self):
        """Test valid alphanumeric problem ID"""
        # Should not raise
        validate_problem_id_format("sumatoria")
        validate_problem_id_format("problema123")
        validate_problem_id_format("test_problem")
        validate_problem_id_format("my-problem")

    def test_invalid_special_characters(self):
        """Test problem ID with invalid special characters"""
        with pytest.raises(ValidationError) as exc_info:
            validate_problem_id_format("problem@123")

        assert "alphanumeric" in str(exc_info.value).lower()

    def test_invalid_spaces(self):
        """Test problem ID with spaces"""
        with pytest.raises(ValidationError) as exc_info:
            validate_problem_id_format("my problem")

        assert "alphanumeric" in str(exc_info.value).lower()

    def test_empty_problem_id(self):
        """Test empty problem ID"""
        with pytest.raises(ValidationError) as exc_info:
            validate_problem_id_format("")

        assert "alphanumeric" in str(exc_info.value).lower()

    def test_valid_with_hyphens_underscores(self):
        """Test valid problem ID with hyphens and underscores"""
        # Should not raise
        validate_problem_id_format("my-test_problem-123")


class TestValidateProblemExists:
    """Test cases for problem existence validation"""

    def test_problem_exists(self, mock_problem_dir, monkeypatch):
        """Test validation when problem exists"""
        from backend.services.problem_service import ProblemService

        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)
        # Should not raise
        validate_problem_exists("sumatoria", service)

    def test_problem_not_exists(self, mock_problem_dir, monkeypatch):
        """Test validation when problem doesn't exist"""
        from backend.services.problem_service import ProblemService

        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)

        with pytest.raises(ProblemNotFoundError) as exc_info:
            validate_problem_exists("nonexistent", service)

        assert "not found" in str(exc_info.value).lower()


class TestValidateSubmissionRequest:
    """Test cases for complete submission request validation"""

    def test_valid_submission(self, mock_problem_dir, monkeypatch):
        """Test valid submission request"""
        from backend.services.problem_service import ProblemService

        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)
        code = "def suma(a, b):\n    return a + b"

        # Should not raise
        validate_submission_request("sumatoria", code, service)

    def test_invalid_problem_id_format(self, mock_problem_dir, monkeypatch):
        """Test submission with invalid problem ID format"""
        from backend.services.problem_service import ProblemService

        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)
        code = "def suma(a, b):\n    return a + b"

        with pytest.raises(ValidationError):
            validate_submission_request("invalid@problem", code, service)

    def test_problem_not_exists(self, mock_problem_dir, monkeypatch):
        """Test submission for non-existent problem"""
        from backend.services.problem_service import ProblemService

        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)
        code = "def suma(a, b):\n    return a + b"

        with pytest.raises(ProblemNotFoundError):
            validate_submission_request("nonexistent", code, service)

    def test_code_too_long(self, mock_problem_dir, monkeypatch):
        """Test submission with code exceeding length limit"""
        from backend.services.problem_service import ProblemService

        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)
        code = "x" * 100000  # Very long code

        with pytest.raises(ValidationError) as exc_info:
            validate_submission_request("sumatoria", code, service, max_code_length=10000)

        assert "exceeds maximum length" in str(exc_info.value)

    def test_dangerous_code(self, mock_problem_dir, monkeypatch):
        """Test submission with dangerous code"""
        from backend.services.problem_service import ProblemService

        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)
        code = "import os\nos.system('rm -rf /')"

        with pytest.raises(ValidationError) as exc_info:
            validate_submission_request("sumatoria", code, service)

        assert "dangerous" in str(exc_info.value).lower()

    def test_all_validations_run_in_order(self, mock_problem_dir, monkeypatch):
        """Test that validations run in correct order"""
        from backend.services.problem_service import ProblemService

        service = ProblemService()
        monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)

        # Invalid format should fail first, before checking existence
        with pytest.raises(ValidationError):
            validate_submission_request("invalid@id", "code", service)
