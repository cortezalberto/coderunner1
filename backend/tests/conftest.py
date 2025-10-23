"""
Pytest configuration and fixtures for backend tests
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models import Submission, TestResult


@pytest.fixture(scope="function")
def test_db():
    """Create an in-memory SQLite database for testing"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def sample_submission_data():
    """Sample submission data for testing"""
    return {
        "job_id": "test-job-123",
        "student_id": "student-001",
        "problem_id": "sumatoria",
        "code": "def suma(a, b):\n    return a + b",
        "status": "pending",
        "ok": None,
        "score_total": 0.0,
        "score_max": 10.0,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "stdout": "",
        "stderr": "",
        "duration_sec": 0.0
    }


@pytest.fixture
def sample_test_result_data():
    """Sample test result data for testing"""
    return {
        "test_name": "test_suma_basico",
        "outcome": "passed",
        "duration": 0.001,
        "message": "",
        "points": 3.0,
        "max_points": 3.0,
        "visibility": "public"
    }


@pytest.fixture
def mock_problem_dir(tmp_path):
    """Create a mock problem directory structure"""
    problem_dir = tmp_path / "sumatoria"
    problem_dir.mkdir()

    # Create metadata.json
    metadata = problem_dir / "metadata.json"
    metadata.write_text('''{
        "title": "Suma Simple",
        "difficulty": "easy",
        "tags": ["basics", "arithmetic"],
        "timeout_sec": 3.0,
        "memory_mb": 128
    }''')

    # Create prompt.md
    prompt = problem_dir / "prompt.md"
    prompt.write_text("# Suma Simple\n\nImplementa suma(a, b)")

    # Create starter.py
    starter = problem_dir / "starter.py"
    starter.write_text("def suma(a, b):\n    pass")

    # Create tests_public.py
    tests_public = problem_dir / "tests_public.py"
    tests_public.write_text("def test_suma():\n    assert True")

    # Create tests_hidden.py
    tests_hidden = problem_dir / "tests_hidden.py"
    tests_hidden.write_text("def test_suma_hidden():\n    assert True")

    # Create rubric.json
    rubric = problem_dir / "rubric.json"
    rubric.write_text('''{
        "tests": [
            {"name": "test_suma_basico", "points": 3, "visibility": "public"},
            {"name": "test_suma_negativos", "points": 2, "visibility": "public"},
            {"name": "test_suma_grande", "points": 5, "visibility": "hidden"}
        ],
        "max_points": 10
    }''')

    return tmp_path
