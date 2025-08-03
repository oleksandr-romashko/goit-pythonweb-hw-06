"""
Database session management module.

This module provides a SQLAlchemy session factory and a context manager for safe session handling.
"""

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

from .connection import engine

SessionFactory = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """
    Provide a transactional scope around a series of operations.

    This context manager creates a new SQLAlchemy session, yields it for use,
    and ensures proper commit or rollback at the end. It also closes the session
    to release database resources.

    Usage:
        with session_scope() as session:
            session.add(obj)
            session.query(MyModel).all()

    Yields:
        sqlalchemy.orm.Session: The SQLAlchemy session object.

    Raises:
        Exception: Re-raises any exception that occurs within the context block
                   after rolling back the transaction.
    """
    session = SessionFactory()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
