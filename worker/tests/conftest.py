"""
Pytest configuration and fixtures for worker tests
"""
import pytest
from pathlib import Path


@pytest.fixture
def sample_test_details():
    """Sample test details from pytest JSON report"""
    return [
        {
            "nodeid": "tests_public.py::test_suma_basico",
            "outcome": "passed",
            "duration": 0.001,
            "longrepr": ""
        },
        {
            "nodeid": "tests_public.py::test_suma_negativos",
            "outcome": "passed",
            "duration": 0.002,
            "longrepr": ""
        },
        {
            "nodeid": "tests_hidden.py::test_suma_grande",
            "outcome": "failed",
            "duration": 0.003,
            "longrepr": "AssertionError: Expected 1000000, got 999999"
        }
    ]


@pytest.fixture
def sample_rubric():
    """Sample rubric for testing"""
    return {
        "tests": [
            {"name": "test_suma_basico", "points": 3, "visibility": "public"},
            {"name": "test_suma_negativos", "points": 2, "visibility": "public"},
            {"name": "test_suma_grande", "points": 5, "visibility": "hidden"}
        ],
        "max_points": 10
    }


@pytest.fixture
def mock_workspace(tmp_path):
    """Create a mock workspace directory"""
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    # Create student code
    student_code = workspace / "student_code.py"
    student_code.write_text("def suma(a, b):\n    return a + b")

    # Create test files
    tests_public = workspace / "tests_public.py"
    tests_public.write_text("""
def test_suma_basico():
    from student_code import suma
    assert suma(2, 3) == 5
""")

    tests_hidden = workspace / "tests_hidden.py"
    tests_hidden.write_text("""
def test_suma_grande():
    from student_code import suma
    assert suma(1000, 2000) == 3000
""")

    # Create conftest
    conftest = workspace / "conftest.py"
    conftest.write_text("""
import pytest
import json

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        pass
""")

    return workspace


@pytest.fixture
def sample_docker_result():
    """Sample Docker execution result"""
    return {
        "stdout": "....\\n4 passed in 0.15s",
        "stderr": "",
        "returncode": 0,
        "duration": 1.5,
        "timed_out": False
    }
