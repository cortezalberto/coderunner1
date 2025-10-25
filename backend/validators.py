"""
Input validation utilities
"""
from fastapi import HTTPException
from pathlib import Path
from .config import settings


def validate_code_length(code: str) -> None:
    """Validate code length doesn't exceed limits"""
    if len(code) > settings.MAX_CODE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Code exceeds maximum length of {settings.MAX_CODE_LENGTH} characters"
        )


def validate_code_safety(code: str) -> None:
    """Basic safety checks for submitted code"""
    # Remove all whitespace characters for bypass detection
    import re
    code_normalized = re.sub(r'\s+', '', code.lower())

    dangerous_patterns = [
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
        "open(",  # Only allow in specific contexts
        "__builtins__",
        "getattr",
        "setattr",
        "delattr",
        "globals(",
        "locals(",
        "vars("
    ]

    for dangerous in dangerous_patterns:
        if dangerous in code_normalized:
            raise HTTPException(
                status_code=400,
                detail=f"Code contains potentially dangerous pattern: {dangerous.replace('import', 'import ')}"
            )


def validate_problem_exists(problem_id: str) -> None:
    """Validate problem directory exists"""
    pdir = Path(settings.PROBLEMS_DIR) / problem_id
    if not pdir.exists():
        # Try fallback path
        pdir = Path("problems") / problem_id
        if not pdir.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Problem '{problem_id}' not found"
            )


def validate_problem_id_format(problem_id: str) -> None:
    """Validate problem_id format"""
    if not problem_id:
        raise HTTPException(status_code=400, detail="problem_id cannot be empty")

    # Only alphanumeric and underscores
    if not problem_id.replace('_', '').replace('-', '').isalnum():
        raise HTTPException(
            status_code=400,
            detail="problem_id must contain only alphanumeric characters, underscores, and hyphens"
        )


def validate_submission_request(req) -> None:
    """Run all validations on submission request"""
    validate_problem_id_format(req.problem_id)
    validate_problem_exists(req.problem_id)
    validate_code_length(req.code)
    validate_code_safety(req.code)
