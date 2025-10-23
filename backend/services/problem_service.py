"""
Problem management service
"""
from typing import Dict, Any, Optional
from pathlib import Path
import json
from ..config import settings
from ..exceptions import ProblemNotFoundError
from ..logging_config import get_logger

logger = get_logger(__name__)


class ProblemService:
    """Service for managing problems"""

    def __init__(self):
        self.problems_dir = Path(settings.PROBLEMS_DIR)

    def get_problem_dir(self, problem_id: str) -> Path:
        """Get problem directory, raise if not exists"""
        pdir = self.problems_dir / problem_id
        if not pdir.exists():
            # Try fallback path
            pdir = Path("problems") / problem_id
            if not pdir.exists():
                raise ProblemNotFoundError(f"Problem {problem_id} not found")
        return pdir

    def list_all(self) -> Dict[str, Dict[str, Any]]:
        """List all available problems with metadata"""
        problems = {}

        if not self.problems_dir.exists():
            # Try fallback
            self.problems_dir = Path("problems")
            if not self.problems_dir.exists():
                logger.warning(f"Problems directory not found: {self.problems_dir}")
                return problems

        for problem_dir in self.problems_dir.iterdir():
            if problem_dir.is_dir() and not problem_dir.name.startswith('.'):
                try:
                    problem_data = self._load_problem_data(problem_dir)
                    problems[problem_dir.name] = problem_data
                except Exception as e:
                    logger.error(f"Error loading problem {problem_dir.name}: {e}")

        logger.info(f"Loaded {len(problems)} problems")
        return problems

    def _load_problem_data(self, problem_dir: Path) -> Dict[str, Any]:
        """Load all data for a single problem"""
        return {
            "metadata": self._load_metadata(problem_dir),
            "prompt": self._load_prompt(problem_dir),
            "starter": self._load_starter(problem_dir)
        }

    def _load_metadata(self, problem_dir: Path) -> Dict[str, Any]:
        """Load metadata.json"""
        meta_path = problem_dir / "metadata.json"
        if not meta_path.exists():
            return {}
        return json.loads(meta_path.read_text(encoding="utf-8"))

    def _load_prompt(self, problem_dir: Path) -> str:
        """Load prompt.md"""
        prompt_path = problem_dir / "prompt.md"
        if not prompt_path.exists():
            return ""
        return prompt_path.read_text(encoding="utf-8")

    def _load_starter(self, problem_dir: Path) -> str:
        """Load starter.py"""
        starter_path = problem_dir / "starter.py"
        if not starter_path.exists():
            return ""
        return starter_path.read_text(encoding="utf-8")

    def get_test_files(self, problem_id: str) -> Dict[str, Optional[Path]]:
        """Get paths to test files"""
        pdir = self.get_problem_dir(problem_id)

        tests_public = pdir / "tests_public.py"
        tests_hidden = pdir / "tests_hidden.py"
        tests_legacy = pdir / "tests.py"

        return {
            "public": tests_public if tests_public.exists() else None,
            "hidden": tests_hidden if tests_hidden.exists() else None,
            "legacy": tests_legacy if tests_legacy.exists() else None
        }

    def load_rubric(self, problem_id: str) -> Dict[str, Any]:
        """Load rubric.json"""
        pdir = self.get_problem_dir(problem_id)
        rubric_path = pdir / "rubric.json"

        if not rubric_path.exists():
            logger.warning(f"No rubric found for problem {problem_id}")
            return {"tests": [], "max_points": 0}

        return json.loads(rubric_path.read_text(encoding="utf-8"))


# Singleton instance
problem_service = ProblemService()
