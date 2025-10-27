"""
RQ Worker tasks for running submissions in Docker sandbox
"""
import tempfile
import shutil
import pathlib
import json
import os
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

# Importar modelos y database
import sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from backend.database import SessionLocal
from backend.models import Submission, TestResult
from backend.config import settings
from backend.logging_config import get_logger

# Importar services
from .services.docker_runner import docker_runner
from .services.rubric_scorer import rubric_scorer

logger = get_logger(__name__)


DEFAULT_TIMEOUT = 5.0  # segundos
DEFAULT_MEMORY_MB = 256
WORKSPACE_DIR = os.getenv("WORKSPACE_DIR", "/workspaces")  # Directorio dentro del worker container


def _copy_test_file(src: pathlib.Path, dest: pathlib.Path, file_type: str) -> None:
    """
    Copy test file with proper permissions and error handling.

    Args:
        src: Source test file path
        dest: Destination path in workspace
        file_type: Type of test file (e.g., "public", "hidden", "legacy")

    Raises:
        Exception: If file copy fails
    """
    try:
        shutil.copy2(src, dest)
        os.chmod(dest, 0o666)
        logger.info(f"Copied {file_type} test file", extra={"src": str(src), "dest": str(dest)})
    except Exception as e:
        logger.error(
            f"Failed to copy {file_type} test file",
            extra={"src": str(src), "dest": str(dest), "error": str(e)}
        )
        raise


def run_submission_in_sandbox(submission_id: int, problem_id: str, code: str,
                               timeout_sec=None, memory_mb=None):
    """
    Execute student code in isolated Docker container.

    PERFORMANCE: Uses connection pooling from backend.database (20 base + 30 overflow).
    Connection is properly closed via try/finally to return to pool.

    Steps:
    1. Create temp workspace
    2. Copy problem tests and rubric
    3. Write student code
    4. Run Docker container with pytest
    5. Parse results and apply rubric
    6. Save to database
    """
    db: Session = SessionLocal()

    try:
        # Validate connection health (pool_pre_ping=True in database.py)
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            logger.error(
                f"Submission {submission_id} not found in database",
                extra={"submission_id": submission_id}
            )
            raise Exception(f"Submission {submission_id} not found")

        # Actualizar estado
        submission.status = "running"
        db.commit()

        # Configuración
        timeout_sec = float(timeout_sec) if timeout_sec else DEFAULT_TIMEOUT
        memory_mb = int(memory_mb) if memory_mb else DEFAULT_MEMORY_MB

        # Buscar metadata del problema usando settings
        problem_dir = pathlib.Path(settings.PROBLEMS_DIR) / problem_id
        if not problem_dir.exists():
            # Fallback para desarrollo local
            problem_dir = pathlib.Path("backend/problems") / problem_id
        if not problem_dir.exists():
            logger.error(
                "Problem directory not found",
                extra={"problem_id": problem_id, "search_paths": [settings.PROBLEMS_DIR, "backend/problems"]}
            )
            raise Exception(f"Problem {problem_id} not found")

        meta_path = problem_dir / "metadata.json"
        rubric_path = problem_dir / "rubric.json"

        # Cargar metadata para override de límites
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            timeout_sec = float(meta.get("timeout_sec", timeout_sec))
            memory_mb = int(meta.get("memory_mb", memory_mb))

        # Crear workspace temporal en directorio compartido con host
        # Esto es necesario para que Docker pueda montar el volumen
        workspace = tempfile.mkdtemp(prefix=f"sandbox-{problem_id}-", dir=WORKSPACE_DIR)
        workspace_path = pathlib.Path(workspace)

        # Dar permisos 777 al workspace para que el usuario sandbox (uid 1000) pueda leer/escribir
        os.chmod(workspace, 0o777)

        try:
            # Escribir código del estudiante
            (workspace_path / "student_code.py").write_text(code, encoding="utf-8")
            os.chmod(workspace_path / "student_code.py", 0o666)

            # Copiar tests públicos y ocultos usando helper function
            tests_public = problem_dir / "tests_public.py"
            tests_hidden = problem_dir / "tests_hidden.py"

            # Si no existen tests_public/hidden, buscar tests.py legacy
            if not tests_public.exists() and not tests_hidden.exists():
                tests_legacy = problem_dir / "tests.py"
                if tests_legacy.exists():
                    _copy_test_file(tests_legacy, workspace_path / "tests_public.py", "legacy")
            else:
                if tests_public.exists():
                    _copy_test_file(tests_public, workspace_path / "tests_public.py", "public")
                if tests_hidden.exists():
                    _copy_test_file(tests_hidden, workspace_path / "tests_hidden.py", "hidden")

            # Copiar conftest.py para generar report.json
            conftest_content = '''"""
Pytest plugin to generate detailed JSON report
"""
import pytest
import json

test_results = []

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        test_results.append({
            "name": item.nodeid,
            "outcome": report.outcome,
            "duration": report.duration,
            "message": str(report.longrepr) if report.longrepr else ""
        })

def pytest_sessionfinish(session, exitstatus):
    with open("/workspace/report.json", "w") as f:
        json.dump(test_results, f, indent=2)
'''
            (workspace_path / "conftest.py").write_text(conftest_content, encoding="utf-8")
            os.chmod(workspace_path / "conftest.py", 0o666)

            # Ejecutar tests en Docker usando DockerRunner service
            docker_result = docker_runner.run(
                workspace=workspace,
                timeout_sec=timeout_sec,
                memory_mb=memory_mb
            )

            stdout = docker_result.stdout
            stderr = docker_result.stderr
            returncode = docker_result.returncode
            duration = docker_result.duration
            timed_out = docker_result.timed_out

            # Leer report.json generado por conftest
            report_path = workspace_path / "report.json"
            test_details = []
            if report_path.exists():
                test_details = json.loads(report_path.read_text(encoding="utf-8"))

            # Cargar rúbrica
            rubric = {"tests": [], "max_points": 0}
            if rubric_path.exists():
                rubric = json.loads(rubric_path.read_text(encoding="utf-8"))

            # Aplicar scoring usando RubricScorer service
            scoring_result = rubric_scorer.score(
                test_details=test_details,
                rubric=rubric
            )

            # Guardar resultados individuales en base de datos
            for test_score in scoring_result.test_scores:
                test_result = TestResult(
                    submission_id=submission_id,
                    test_name=test_score.test_name,
                    outcome=test_score.outcome,
                    duration=test_score.duration,
                    message=test_score.message,
                    points=test_score.points,
                    max_points=test_score.max_points,
                    visibility=test_score.visibility
                )
                db.add(test_result)

            # Actualizar submission usando datos del scoring_result
            submission.status = "timeout" if timed_out else "completed"
            submission.ok = (returncode == 0 and not timed_out)
            submission.score_total = scoring_result.score_total
            submission.score_max = scoring_result.score_max
            submission.passed = scoring_result.passed
            submission.failed = scoring_result.failed
            submission.errors = scoring_result.errors
            submission.duration_sec = round(duration, 4)
            submission.stdout = stdout[:10000]  # limitar tamaño
            submission.stderr = stderr[:10000]
            submission.completed_at = datetime.utcnow()

            if timed_out:
                submission.error_message = f"Execution timeout ({timeout_sec}s)"

            db.commit()

        finally:
            # Limpiar workspace
            shutil.rmtree(workspace, ignore_errors=True)

    except Exception as e:
        # Marcar como fallado
        logger.error(
            f"Submission {submission_id} failed with error: {str(e)}",
            extra={"submission_id": submission_id, "problem_id": problem_id},
            exc_info=True
        )
        try:
            submission.status = "failed"
            submission.error_message = str(e)[:1000]
            submission.completed_at = datetime.utcnow()
            db.commit()
        except Exception as commit_error:
            logger.error(
                f"Failed to save error status for submission {submission_id}",
                extra={"submission_id": submission_id, "error": str(commit_error)},
                exc_info=True
            )
            db.rollback()
        raise

    finally:
        # CRITICAL: Always close DB connection to return to pool
        # Without this, connections leak and pool gets exhausted
        db.close()
        logger.debug(
            f"DB connection closed for submission {submission_id}",
            extra={"submission_id": submission_id}
        )
