"""
Database Connection Manager
SQLAlchemy (sync) configuration with proper session management
"""

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from sqlalchemy import Connection, Engine, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.shared.config import settings


# Base class for all models
class Base(DeclarativeBase):
    pass


class DatabaseSessionManager:
    """
    Database session manager with context managers.
    Provides proper resource management for connections and sessions.
    """

    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None):
        engine_kwargs = dict(engine_kwargs or {})

        if host.startswith("sqlite"):
            engine_kwargs.setdefault("connect_args", {"check_same_thread": False})

        self._engine: Engine | None = create_engine(host, **engine_kwargs)
        self._sessionmaker: sessionmaker[Session] | None = sessionmaker(
            bind=self._engine
        )

    def close(self) -> None:
        """Close database engine and cleanup resources"""
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextmanager
    def connect(self) -> Iterator[Connection]:
        """
        Context manager for database connections.
        Use for raw SQL operations or migrations.
        Commits on success and rolls back on error (engine.begin() does both).
        """
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        with self._engine.begin() as connection:
            yield connection

    @contextmanager
    def session(self) -> Iterator[Session]:
        """
        Context manager for database sessions.
        Use for ORM operations (recommended for most cases).
        """
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def test_connection(self) -> None:
        """Test database connection"""
        try:
            with self.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database connection established")
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise


# Initialize global session manager
sessionmanager = DatabaseSessionManager(settings.database_url)


def get_db() -> Iterator[Session]:
    """
    Dependency for FastAPI to get a database session.

    Usage:
        def endpoint(session: Session = Depends(get_db)):
            # Your code here
    """
    with sessionmanager.session() as session:
        yield session