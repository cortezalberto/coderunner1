"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime


# ==================== Request Schemas ====================

class SubmissionRequest(BaseModel):
    """Schema for code submission request"""
    problem_id: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=50000)
    student_id: Optional[str] = Field(None, max_length=100)
    timeout_sec: Optional[float] = Field(None, gt=0, le=30)
    memory_mb: Optional[int] = Field(None, gt=0, le=1024)

    @field_validator('problem_id')
    @classmethod
    def validate_problem_id(cls, v):
        """Validate problem_id format"""
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('problem_id must contain only alphanumeric characters, underscores, and hyphens')
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "problem_id": "sumatoria",
                "code": "def suma(a, b):\\n    return a + b",
                "student_id": "student123"
            }
        }
    )


# ==================== Response Schemas ====================

class SubmissionResponse(BaseModel):
    """Schema for submission response"""
    job_id: str
    status: str
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "job_id": "abc123-def456",
                "status": "queued",
                "message": "Submission enqueued successfully"
            }
        }
    )


class TestResultSchema(BaseModel):
    """Schema for individual test result"""
    test_name: str
    outcome: str
    duration: float
    message: str
    points: float
    max_points: float
    visibility: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "test_name": "test_suma_basico",
                "outcome": "passed",
                "duration": 0.001,
                "message": "",
                "points": 3.0,
                "max_points": 3.0,
                "visibility": "public"
            }
        }
    )


class ResultResponse(BaseModel):
    """Schema for submission result response"""
    job_id: str
    status: str
    ok: Optional[bool] = None
    score_total: Optional[float] = None
    score_max: Optional[float] = None
    passed: Optional[int] = None
    failed: Optional[int] = None
    errors: Optional[int] = None
    duration_sec: Optional[float] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    error_message: Optional[str] = None
    test_results: Optional[List[TestResultSchema]] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProblemMetadata(BaseModel):
    """Schema for problem metadata"""
    title: str
    difficulty: str
    tags: List[str]
    timeout_sec: float
    memory_mb: int


class Problem(BaseModel):
    """Schema for a single problem"""
    metadata: ProblemMetadata
    prompt: str
    starter: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "metadata": {
                    "title": "Suma Simple",
                    "difficulty": "easy",
                    "tags": ["basics", "arithmetic"],
                    "timeout_sec": 3.0,
                    "memory_mb": 128
                },
                "prompt": "# Problema: Suma Simple\\n\\nImplementa una función suma(a, b)...",
                "starter": "def suma(a, b):\\n    pass"
            }
        }
    )


class SubmissionSummary(BaseModel):
    """Schema for submission summary in admin panel"""
    id: int
    job_id: str
    student_id: Optional[str]
    problem_id: str
    status: str
    ok: Optional[bool]
    score_total: Optional[float]
    score_max: Optional[float]
    passed: Optional[int]
    failed: Optional[int]
    errors: Optional[int]
    duration_sec: Optional[float]
    created_at: datetime
    completed_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class ProblemStats(BaseModel):
    """Schema for problem statistics"""
    problem_id: str
    submissions: int
    avg_score: float


class AdminSummary(BaseModel):
    """Schema for admin summary statistics"""
    total_submissions: int
    completed: int
    failed: int
    pending: int
    avg_score: float
    by_problem: List[ProblemStats]


class SubmissionsListResponse(BaseModel):
    """Schema for paginated submissions list"""
    total: int
    limit: int
    offset: int
    submissions: List[SubmissionSummary]
