"""
Problem management service
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import json
from ..config import settings
from ..exceptions import ProblemNotFoundError, ValidationError
from ..logging_config import get_logger

logger = get_logger(__name__)


class ProblemService:
    """Service for managing problems"""

    def __init__(self):
        self.problems_dir = self._resolve_problems_dir()
        self._subject_service = None  # Lazy load to avoid circular import

    def _resolve_problems_dir(self) -> Path:
        """Resolve problems directory with fallback logic"""
        primary = Path(settings.PROBLEMS_DIR)
        if primary.exists():
            return primary

        fallback = Path("problems")
        if fallback.exists():
            logger.warning(f"Using fallback problems dir: {fallback}")
            return fallback

        raise ProblemNotFoundError(
            f"Problems directory not found. Tried: {primary}, {fallback}"
        )

    @property
    def subject_service(self):
        """Lazy load SubjectService to avoid circular import"""
        if self._subject_service is None:
            from .subject_service import subject_service
            self._subject_service = subject_service
        return self._subject_service

    def get_problem_dir(self, problem_id: str) -> Path:
        """Get problem directory, raise if not exists"""
        pdir = self.problems_dir / problem_id
        if not pdir.exists():
            raise ProblemNotFoundError(f"Problem {problem_id} not found in {self.problems_dir}")
        return pdir

    def _validate_problem_metadata(self, problem_id: str, metadata: Dict[str, Any]) -> None:
        """Validate problem metadata against subjects config"""
        subject_id = metadata.get("subject_id")
        unit_id = metadata.get("unit_id")

        if not subject_id or not unit_id:
            logger.warning(
                f"Problem {problem_id} missing subject_id or unit_id",
                extra={"problem_id": problem_id}
            )
            return

        # Validate subject exists
        try:
            subject = self.subject_service.get_subject(subject_id)
            if not subject:
                logger.error(
                    f"Problem {problem_id} has invalid subject_id: {subject_id}",
                    extra={"problem_id": problem_id, "subject_id": subject_id}
                )
                return

            # Validate unit exists in subject
            if not self.subject_service.validate_subject_unit(subject_id, unit_id):
                logger.error(
                    f"Problem {problem_id} has invalid unit_id: {unit_id} for subject: {subject_id}",
                    extra={"problem_id": problem_id, "subject_id": subject_id, "unit_id": unit_id}
                )
                return

            logger.debug(
                f"Problem {problem_id} metadata validated successfully",
                extra={"problem_id": problem_id, "subject_id": subject_id, "unit_id": unit_id}
            )
        except Exception as e:
            logger.error(
                f"Error validating problem {problem_id} metadata: {e}",
                extra={"problem_id": problem_id},
                exc_info=True
            )

    def list_all(self) -> Dict[str, Dict[str, Any]]:
        """List all available problems with metadata"""
        problems = {}

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
        metadata = self._load_metadata(problem_dir)

        # Validate metadata
        self._validate_problem_metadata(problem_dir.name, metadata)

        return {
            "metadata": metadata,
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

    def list_by_subject_and_unit(
        self, subject_id: Optional[str] = None, unit_id: Optional[str] = None
    ) -> Dict[str, Dict[str, Any]]:
        """List problems filtered by subject and/or unit"""
        all_problems = self.list_all()

        if not subject_id and not unit_id:
            return all_problems

        filtered = {}
        for problem_id, problem_data in all_problems.items():
            metadata = problem_data.get("metadata", {})

            # Filter by subject
            if subject_id and metadata.get("subject_id") != subject_id:
                continue

            # Filter by unit
            if unit_id and metadata.get("unit_id") != unit_id:
                continue

            filtered[problem_id] = problem_data

        logger.info(
            f"Filtered problems: subject={subject_id}, unit={unit_id}, "
            f"found={len(filtered)}"
        )
        return filtered

    def group_by_subject_and_unit(self) -> Dict[str, Dict[str, List[str]]]:
        """Group problem IDs by subject and unit"""
        all_problems = self.list_all()
        grouped = {}

        for problem_id, problem_data in all_problems.items():
            metadata = problem_data.get("metadata", {})
            subject_id = metadata.get("subject_id", "uncategorized")
            unit_id = metadata.get("unit_id", "general")

            if subject_id not in grouped:
                grouped[subject_id] = {}

            if unit_id not in grouped[subject_id]:
                grouped[subject_id][unit_id] = []

            grouped[subject_id][unit_id].append(problem_id)

        return grouped


# Singleton instance
problem_service = ProblemService()
