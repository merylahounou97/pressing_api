# Dependency
from sqlalchemy.orm import Session
from src.database import SessionLocal


def get_db():
    """Get the database session.

    Yields:
        Session: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
