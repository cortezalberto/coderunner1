"""
Database configuration and session management

PERFORMANCE: Configured with connection pooling for 300 concurrent users.
- pool_size=20: Base connection pool
- max_overflow=30: Additional connections under load (total: 50)
- pool_timeout=30: Wait time for available connection
- pool_pre_ping=True: Validate connections before use
- pool_recycle=3600: Recycle connections every hour
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from .config import settings

# Production-ready connection pool configuration
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,              # Base number of connections to keep open
    max_overflow=30,           # Max additional connections under load
    pool_timeout=30,           # Seconds to wait for available connection
    pool_pre_ping=True,        # Test connection health before using
    pool_recycle=3600,         # Recycle connections after 1 hour
    echo_pool=False,           # Disable pool logging in production
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency for FastAPI endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
