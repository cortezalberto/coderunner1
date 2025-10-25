"""
Input validation utilities for code submission and problem management.

This module provides validators for:
- Code length limits
- Security checks (dangerous imports/functions)
- Problem ID format and existence
"""
import re
from pathlib import Path
from typing import Any

from .config import settings
from .exceptions import ValidationError
from .logging_config import get_logger

logger = get_logger(__name__)

# Compile regex patterns at module level for performance
_WHITESPACE_PATTERN = re.compile(r'\s+')
_PROBLEM_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')

# Dangerous patterns that should be blocked in student code
_DANGEROUS_PATTERNS = frozenset([
    # Dangerous imports
    "importos",
    "importsubprocess",
    "importsys",
    "importsocket",
    "importrequests",
    "importurllib",
    "importshutil",
    "importglob",
    "importpickle",
    "importtempfile",
    # From imports
    "fromosimport",
    "fromsubprocessimport",
    "fromsysimport",
    # Built-in dangerous functions
    "__import__",
    "exec(",
    "eval(",
    "compile(",
    "open(",
    "__builtins__",
    "getattr",
    "setattr",
    "delattr",
    "globals(",
    "locals(",
    "vars("
])


def validate_code_length(code: str) -> None:
    """
    Validate that submitted code doesn't exceed maximum length.

    Args:
        code: The source code to validate

    Raises:
        ValidationError: If code exceeds MAX_CODE_LENGTH
    """
    if len(code) > settings.MAX_CODE_LENGTH:
        logger.warning(
            "Code length validation failed",
            extra={"code_length": len(code), "max_length": settings.MAX_CODE_LENGTH}
        )
        raise ValidationError(
            f"Code exceeds maximum length of {settings.MAX_CODE_LENGTH} characters"
        )


def validate_code_safety(code: str) -> None:
    """
    Perform basic security checks on submitted code.

    Validates that code doesn't contain dangerous imports or built-in functions
    that could compromise the sandbox environment.

    Args:
        code: The source code to validate

    Raises:
        ValidationError: If code contains dangerous patterns
    """
    # Remove all whitespace characters for bypass detection
    code_normalized = _WHITESPACE_PATTERN.sub('', code.lower())

    for dangerous_pattern in _DANGEROUS_PATTERNS:
        if dangerous_pattern in code_normalized:
            # Format the pattern for better error message
            formatted_pattern = dangerous_pattern.replace('import', 'import ')
            logger.warning(
                "Dangerous code pattern detected",
                extra={"pattern": formatted_pattern, "code_preview": code[:100]}
            )
            raise ValidationError(
                f"Code contains potentially dangerous pattern: {formatted_pattern}"
            )


def validate_problem_exists(problem_id: str) -> None:
    """
    Validate that a problem directory exists.

    Checks the configured PROBLEMS_DIR first, then falls back to relative path.

    Args:
        problem_id: The problem identifier

    Raises:
        ValidationError: If problem directory doesn't exist
    """
    pdir = Path(settings.PROBLEMS_DIR) / problem_id
    if not pdir.exists():
        # Try fallback path for local development
        pdir = Path("problems") / problem_id
        if not pdir.exists():
            logger.error(
                "Problem not found",
                extra={"problem_id": problem_id, "search_paths": [settings.PROBLEMS_DIR, "problems"]}
            )
            raise ValidationError(f"Problem '{problem_id}' not found")


def validate_problem_id_format(problem_id: str) -> None:
    """
    Validate problem_id format.

    Problem IDs must:
    - Not be empty
    - Contain only alphanumeric characters, underscores, and hyphens

    Args:
        problem_id: The problem identifier to validate

    Raises:
        ValidationError: If format is invalid
    """
    if not problem_id:
        raise ValidationError("problem_id cannot be empty")

    # Use pre-compiled regex pattern
    if not _PROBLEM_ID_PATTERN.match(problem_id):
        logger.warning(
            "Invalid problem_id format",
            extra={"problem_id": problem_id}
        )
        raise ValidationError(
            "problem_id must contain only alphanumeric characters, underscores, and hyphens"
        )


def validate_submission_request(req: Any) -> None:
    """
    Run all validations on a submission request.

    Validates in order:
    1. Problem ID format
    2. Problem existence
    3. Code length
    4. Code safety

    Args:
        req: The submission request object with problem_id and code attributes

    Raises:
        ValidationError: If any validation fails
    """
    validate_problem_id_format(req.problem_id)
    validate_problem_exists(req.problem_id)
    validate_code_length(req.code)
    validate_code_safety(req.code)
