# core/database.py
from collections.abc import Generator
from contextlib import contextmanager
from functools import lru_cache

from prefect_sqlalchemy import SqlAlchemyConnector
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.orm import Session, sessionmaker

from core.config import settings


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """
    Loads the Prefect block and returns the SQLAlchemy Engine.
    lru_cache ensures this executes only ONCE per process runtime.
    """
    connector = SqlAlchemyConnector.load(settings.block_name)
    return connector.get_engine()


@lru_cache(maxsize=1)
def get_session_factory() -> sessionmaker[Session]:
    """Creates a cached session factory bound to the engine."""
    engine = get_engine()
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager providing a transactional ORM session.
    Automatically commits on success, rolls back on error, and closes the session.
    """
    session_factory = get_session_factory()
    session = session_factory()

    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def get_db_connection() -> Generator[Connection, None, None]:
    """Provides a raw pooled connection for fast DataFrame reads."""
    with get_engine().connect() as conn:
        yield conn
