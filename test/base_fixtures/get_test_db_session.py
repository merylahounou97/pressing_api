import pytest
from src.database import SessionLocal

@pytest.fixture(scope="session")
def get_test_db_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()