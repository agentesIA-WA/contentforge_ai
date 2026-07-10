"""Database engine and session lifecycle helpers."""

from collections.abc import Generator
import logging

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and guarantee it is closed."""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError:
        logger.exception("Database session failed")
        db.rollback()
        raise
    finally:
        db.close()


def check_database_connection() -> bool:
    """Return whether the configured database accepts a simple query."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError:
        logger.exception("Database health check failed")
        return False

