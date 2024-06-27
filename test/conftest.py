from unittest.mock import MagicMock
import pytest
from src.database import SessionLocal
from src.users.user_schemas import IdentifierEnum
from .test_init import client


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
def get_access_token(mock_user):
    """Fixture pour récupérer un token d'accès"""

    user = mock_user(IdentifierEnum.EMAIL)

    def _access_token(
        identifier=user["email"],
        password=user["password"],
    ):
        response = client.post(
            "/token",
            data={"username": identifier, "password": password},
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
        )
        response_payload = response.json()
        return response_payload["access_token"]

    return _access_token
