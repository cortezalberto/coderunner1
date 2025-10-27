"""
RQ Scheduler for periodic tasks.

PERFORMANCE: Automated maintenance tasks to prevent resource exhaustion.
- Workspace cleanup: Every 30 minutes
- Removes orphaned sandbox directories older than 1 hour
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from redis import Redis
from rq_scheduler import Scheduler
from backend.config import settings
from backend.logging_config import get_logger

logger = get_logger(__name__)

# Redis connection
redis_conn = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)

# Create scheduler
scheduler = Scheduler(connection=redis_conn, interval=60)


def schedule_periodic_tasks():
    """
    Schedule all periodic maintenance tasks.

    This function should be called once on worker startup.
    """
    logger.info("Scheduling periodic tasks...")

    # Clear any existing scheduled jobs to avoid duplicates
    for job in scheduler.get_jobs():
        logger.info(f"Removing existing job: {job.id}")
        scheduler.cancel(job)

    # Schedule workspace cleanup every 30 minutes
    scheduler.cron(
        cron_string="*/30 * * * *",  # Every 30 minutes
        func="worker.services.workspace_cleaner.cleanup_old_workspaces",
        queue_name="maintenance",
        timeout="5m",
        id="cleanup_workspaces"
    )

    logger.info("Scheduled: workspace cleanup (every 30 minutes)")

    logger.info("All periodic tasks scheduled successfully")


if __name__ == "__main__":
    schedule_periodic_tasks()
    print("Periodic tasks scheduled. Run RQ worker to process them:")
    print("  rq worker --url redis://redis:6379/0 submissions maintenance")
