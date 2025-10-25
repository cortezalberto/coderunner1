"""
Centralized configuration for the application
"""
import os
from typing import List


class Settings:
    """Application settings with environment variable support"""

    # Database
    # Use postgres service name for Docker, localhost for local development
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://playground:playground@postgres:5432/playground"
    )

    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))

    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # CORS
    _cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
    CORS_ORIGINS: List[str] = [origin.strip() for origin in _cors_origins.split(",")]

    # Docker Runner
    RUNNER_IMAGE: str = os.getenv("RUNNER_IMAGE", "py-playground-runner:latest")
    DEFAULT_TIMEOUT_SEC: float = float(os.getenv("DEFAULT_TIMEOUT_SEC", "5.0"))
    DEFAULT_MEMORY_MB: int = int(os.getenv("DEFAULT_MEMORY_MB", "256"))
    DEFAULT_CPUS: str = os.getenv("DEFAULT_CPUS", "1.0")

    # Limits
    MAX_CODE_LENGTH: int = int(os.getenv("MAX_CODE_LENGTH", "50000"))
    MAX_SUBMISSION_POLL_ATTEMPTS: int = int(os.getenv("MAX_POLL_ATTEMPTS", "30"))
    POLL_INTERVAL_SEC: float = float(os.getenv("POLL_INTERVAL_SEC", "1.0"))

    # Paths
    PROBLEMS_DIR: str = os.getenv("PROBLEMS_DIR", "backend/problems")
    BACKEND_DIR: str = os.getenv("BACKEND_DIR", "backend")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


# Singleton instance
settings = Settings()
