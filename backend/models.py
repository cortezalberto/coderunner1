"""
SQLAlchemy models for submissions and test results

PERFORMANCE: Composite indexes for 300 concurrent users
- (status, created_at): Optimizes status filtering + ordering (admin queries)
- (problem_id, status): Optimizes per-problem statistics (admin panel)
- (student_id, created_at): Optimizes student submission history
- (problem_id, created_at): Optimizes problem submission history
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(255), unique=True, index=True, nullable=False)
    student_id = Column(String(255), index=True, nullable=True)  # opcional
    problem_id = Column(String(255), index=True, nullable=False)
    code = Column(Text, nullable=False)

    # Resultados
    status = Column(String(50), default="pending", index=True)  # pending, running, completed, failed, timeout
    ok = Column(Boolean, default=False)
    score_total = Column(Float, default=0.0)
    score_max = Column(Float, default=0.0)

    passed = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    errors = Column(Integer, default=0)

    duration_sec = Column(Float, nullable=True)
    stdout = Column(Text, default="")
    stderr = Column(Text, default="")
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relación con resultados de tests individuales
    test_results = relationship("TestResult", back_populates="submission", cascade="all, delete-orphan")

    # Composite indexes for query optimization
    __table_args__ = (
        # Optimizes: ORDER BY created_at DESC WHERE status = 'X'
        Index('idx_status_created', 'status', 'created_at'),

        # Optimizes: GROUP BY problem_id WHERE status = 'completed'
        Index('idx_problem_status', 'problem_id', 'status'),

        # Optimizes: WHERE student_id = 'X' ORDER BY created_at DESC
        Index('idx_student_created', 'student_id', 'created_at'),

        # Optimizes: WHERE problem_id = 'X' ORDER BY created_at DESC
        Index('idx_problem_created', 'problem_id', 'created_at'),
    )


class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False, index=True)

    test_name = Column(String(255), nullable=False)
    outcome = Column(String(50), nullable=False)  # passed, failed, error, skipped
    duration = Column(Float, default=0.0)
    message = Column(Text, nullable=True)

    # Rúbrica
    points = Column(Float, default=0.0)
    max_points = Column(Float, default=0.0)
    visibility = Column(String(50), default="public")  # public, hidden

    submission = relationship("Submission", back_populates="test_results")
