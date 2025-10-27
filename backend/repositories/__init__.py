"""
Repositories package

Data access layer for the application.
Repositories encapsulate all database queries and provide a clean interface
for services to interact with the data layer.
"""

from .submission_repository import SubmissionRepository, submission_repository
from .test_result_repository import TestResultRepository, test_result_repository

__all__ = [
    'SubmissionRepository',
    'submission_repository',
    'TestResultRepository',
    'test_result_repository',
]
