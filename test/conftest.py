from unittest.mock import MagicMock
import pytest
from src.dependencies.db import get_db
from .test_init import client
from src.database import SessionLocal


@pytest.fixture
def mock_db_session():
    """Fixture pour simuler une session de base de données"""
    return MagicMock()

@pytest.fixture
def get_test_db_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture
def access_token(mock_customer_with_email):
    response = client.post("/token",data={
        "username": mock_customer_with_email["email"],
        "password": mock_customer_with_email["password"],
    }, headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    })

    response_payload = response.json()
    return response_payload["access_token"]