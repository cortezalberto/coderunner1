"""
Workspace cleanup service for orphaned sandbox directories.

PERFORMANCE: Prevents disk space exhaustion from failed cleanup operations.
- Runs every 30 minutes via RQ scheduler
- Deletes workspaces older than 1 hour
- Uses file modification time to detect orphans
"""
import os
import shutil
import time
from pathlib import Path
from typing import List, Tuple
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.logging_config import get_logger
from backend.config import settings

logger = get_logger(__name__)

WORKSPACE_DIR = os.getenv("WORKSPACE_DIR", "/workspaces")
MAX_AGE_SECONDS = 3600  # 1 hour
CLEANUP_BATCH_SIZE = 100


class WorkspaceCleaner:
    """Service for cleaning up orphaned workspace directories"""

    def __init__(self, workspace_dir: str = WORKSPACE_DIR):
        self.workspace_dir = Path(workspace_dir)

    def find_old_workspaces(self, max_age_seconds: int = MAX_AGE_SECONDS) -> List[Path]:
        """
        Find workspace directories older than max_age_seconds.

        Args:
            max_age_seconds: Maximum age in seconds (default: 1 hour)

        Returns:
            List of Path objects for old workspaces
        """
        if not self.workspace_dir.exists():
            logger.warning(
                f"Workspace directory does not exist: {self.workspace_dir}",
                extra={"workspace_dir": str(self.workspace_dir)}
            )
            return []

        old_workspaces = []
        current_time = time.time()
        cutoff_time = current_time - max_age_seconds

        try:
            for entry in self.workspace_dir.iterdir():
                # Only consider directories starting with "sandbox-"
                if not entry.is_dir() or not entry.name.startswith("sandbox-"):
                    continue

                try:
                    # Get directory modification time
                    mtime = entry.stat().st_mtime

                    if mtime < cutoff_time:
                        old_workspaces.append(entry)
                        logger.debug(
                            f"Found old workspace: {entry.name}",
                            extra={
                                "workspace": entry.name,
                                "age_seconds": int(current_time - mtime)
                            }
                        )
                except OSError as e:
                    logger.warning(
                        f"Could not stat workspace {entry.name}: {e}",
                        extra={"workspace": entry.name}
                    )
                    continue

        except Exception as e:
            logger.error(
                f"Error scanning workspace directory: {e}",
                extra={"workspace_dir": str(self.workspace_dir)},
                exc_info=True
            )

        return old_workspaces

    def cleanup_workspace(self, workspace: Path) -> Tuple[bool, str]:
        """
        Delete a single workspace directory.

        Args:
            workspace: Path to workspace directory

        Returns:
            Tuple of (success: bool, error_message: str)
        """
        try:
            shutil.rmtree(workspace, ignore_errors=False)
            logger.info(
                f"Deleted workspace: {workspace.name}",
                extra={"workspace": workspace.name}
            )
            return True, ""
        except Exception as e:
            error_msg = str(e)
            logger.error(
                f"Failed to delete workspace {workspace.name}: {error_msg}",
                extra={"workspace": workspace.name},
                exc_info=True
            )
            return False, error_msg

    def cleanup_all(self, max_age_seconds: int = MAX_AGE_SECONDS) -> dict:
        """
        Find and delete all old workspaces.

        Args:
            max_age_seconds: Maximum age in seconds (default: 1 hour)

        Returns:
            Dictionary with cleanup statistics
        """
        logger.info(
            f"Starting workspace cleanup (max_age={max_age_seconds}s)",
            extra={"workspace_dir": str(self.workspace_dir)}
        )

        old_workspaces = self.find_old_workspaces(max_age_seconds)

        if not old_workspaces:
            logger.info("No old workspaces found")
            return {
                "found": 0,
                "deleted": 0,
                "failed": 0,
                "errors": []
            }

        deleted = 0
        failed = 0
        errors = []

        # Limit batch size to prevent long-running jobs
        workspaces_to_clean = old_workspaces[:CLEANUP_BATCH_SIZE]

        for workspace in workspaces_to_clean:
            success, error_msg = self.cleanup_workspace(workspace)
            if success:
                deleted += 1
            else:
                failed += 1
                errors.append(f"{workspace.name}: {error_msg}")

        result = {
            "found": len(old_workspaces),
            "deleted": deleted,
            "failed": failed,
            "errors": errors
        }

        logger.info(
            f"Workspace cleanup completed",
            extra=result
        )

        return result


# Singleton instance
workspace_cleaner = WorkspaceCleaner()


def cleanup_old_workspaces():
    """
    RQ job function for scheduled cleanup.

    This function is called by RQ scheduler every 30 minutes.
    """
    return workspace_cleaner.cleanup_all()
