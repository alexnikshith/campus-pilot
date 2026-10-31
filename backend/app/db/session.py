from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator, Tuple
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# Base declarative class for all SQLAlchemy models
Base = declarative_base()

# Configure SQLAlchemy engine
# When running with PostgreSQL, use pool_pre_ping to automatically recover dropped connections
engine_args = {
    "pool_pre_ping": True,
}

if settings.sync_database_url.startswith("postgresql"):
    engine_args["pool_size"] = settings.DATABASE_POOL_SIZE
    engine_args["max_overflow"] = settings.DATABASE_MAX_OVERFLOW

engine = create_engine(settings.sync_database_url, **engine_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Dependency that yields an active database session and ensures closure."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_db_connection() -> Tuple[bool, str]:
    """
    Safely verifies database connectivity by executing a lightweight query.
    Returns (True, 'Connected') or (False, 'error description') without leaking credentials.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, "Database connection successful"
    except Exception as exc:
        # Sanitize exception message to avoid exposing sensitive connection URLs
        error_type = type(exc).__name__
        logger.warning(f"Database connectivity check failed: {error_type}")
        return False, f"Database connectivity unavailable ({error_type})"
