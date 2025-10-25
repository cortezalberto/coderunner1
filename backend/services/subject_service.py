"""
Subject and Unit management service
"""
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
from ..config import settings
from ..logging_config import get_logger

logger = get_logger(__name__)


class SubjectService:
    """Service for managing subjects and thematic units"""

    def __init__(self):
        self.config_file = Path(settings.BACKEND_DIR) / "subjects_config.json"
        self._subjects_cache = None

    def _load_subjects_config(self) -> Dict[str, Any]:
        """Load subjects configuration from JSON file"""
        if self._subjects_cache is not None:
            return self._subjects_cache

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

                # Validate structure
                if not isinstance(config, dict):
                    raise ValueError("Config must be a dictionary")

                if "subjects" not in config:
                    raise ValueError("Config missing 'subjects' key")

                if not isinstance(config["subjects"], list):
                    raise ValueError("'subjects' must be a list")

                # Validate each subject has required fields
                for idx, subject in enumerate(config["subjects"]):
                    if not isinstance(subject, dict):
                        raise ValueError(f"Subject at index {idx} must be a dictionary")

                    required_fields = ["id", "name", "units"]
                    for field in required_fields:
                        if field not in subject:
                            raise ValueError(f"Subject at index {idx} missing required field: {field}")

                    if not isinstance(subject["units"], list):
                        raise ValueError(f"Subject '{subject['id']}' units must be a list")

                    # Validate each unit
                    for unit_idx, unit in enumerate(subject["units"]):
                        if not isinstance(unit, dict):
                            raise ValueError(
                                f"Unit at index {unit_idx} in subject '{subject['id']}' must be a dictionary"
                            )

                        unit_required = ["id", "name"]
                        for field in unit_required:
                            if field not in unit:
                                raise ValueError(
                                    f"Unit at index {unit_idx} in subject '{subject['id']}' "
                                    f"missing required field: {field}"
                                )

                self._subjects_cache = config
                logger.info(f"Loaded {len(config['subjects'])} subjects from config")
                return config

        except FileNotFoundError:
            logger.critical(f"FATAL: Subjects config file not found: {self.config_file}")
            raise
        except json.JSONDecodeError as e:
            logger.critical(f"FATAL: Invalid JSON in subjects config: {e}")
            raise
        except ValueError as e:
            logger.critical(f"FATAL: Invalid subjects config structure: {e}")
            raise
        except Exception as e:
            logger.critical(f"FATAL: Error loading subjects config: {e}", exc_info=True)
            raise

    def list_all_subjects(self) -> List[Dict[str, Any]]:
        """Get list of all subjects"""
        config = self._load_subjects_config()
        subjects = config.get("subjects", [])

        # Return subjects without units for the main list
        return [
            {
                "id": subject["id"],
                "name": subject["name"],
                "description": subject.get("description", ""),
                "unit_count": len(subject.get("units", []))
            }
            for subject in subjects
        ]

    def get_subject(self, subject_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific subject with its units"""
        config = self._load_subjects_config()
        subjects = config.get("subjects", [])

        for subject in subjects:
            if subject["id"] == subject_id:
                return subject

        return None

    def list_units_by_subject(self, subject_id: str) -> List[Dict[str, Any]]:
        """Get all units for a specific subject"""
        subject = self.get_subject(subject_id)

        if not subject:
            logger.warning(f"Subject not found: {subject_id}")
            return []

        units = subject.get("units", [])
        # Sort by order
        units_sorted = sorted(units, key=lambda x: x.get("order", 999))

        return units_sorted

    def get_unit(self, subject_id: str, unit_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific unit within a subject"""
        subject = self.get_subject(subject_id)

        if not subject:
            return None

        units = subject.get("units", [])
        for unit in units:
            if unit["id"] == unit_id:
                return unit

        return None

    def get_hierarchy(self) -> Dict[str, Any]:
        """Get complete hierarchy: subjects -> units"""
        config = self._load_subjects_config()
        subjects = config.get("subjects", [])

        hierarchy = {}
        for subject in subjects:
            hierarchy[subject["id"]] = {
                "name": subject["name"],
                "description": subject.get("description", ""),
                "units": {
                    unit["id"]: {
                        "name": unit["name"],
                        "description": unit.get("description", ""),
                        "order": unit.get("order", 999)
                    }
                    for unit in subject.get("units", [])
                }
            }

        return hierarchy

    def validate_subject_unit(self, subject_id: str, unit_id: str) -> bool:
        """Validate that a unit belongs to a subject"""
        unit = self.get_unit(subject_id, unit_id)
        return unit is not None


# Singleton instance
subject_service = SubjectService()
