"""
Custom exceptions for better error handling
"""


class ProblemNotFoundError(Exception):
    """Problem directory not found"""
    pass


class TestExecutionError(Exception):
    """Error during test execution"""
    pass


class DockerExecutionError(Exception):
    """Error executing Docker container"""
    pass


class RubricError(Exception):
    """Error loading or applying rubric"""
    pass


class ValidationError(Exception):
    """Input validation error"""
    pass
