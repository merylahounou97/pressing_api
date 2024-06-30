from unittest.mock import MagicMock
import pytest
from src.database import SessionLocal
from src.lifespans.create_default_admin import create_default_admin_lifespan
from src.users.user_schemas import IdentifierEnum
from src.database import Base, engine
from src.users.user_service import UserService
from .test_init import client
from src.main import app



@pytest.fixture
def mock_db_session():
    """Fixture pour simuler une session de base de données"""
    return MagicMock()


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session",autouse=True)
def setup_and_teardown():

    yield
    Base.metadata.drop_all(bind=engine)

