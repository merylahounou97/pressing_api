from datetime import datetime, timedelta
from unittest.mock import MagicMock
import uuid

import pytest
from src.database import SessionLocal
from src.users.users_model import UserRole
from src.users.users_schemas import IdentifierEnum, UserCreateInput, UserCreateMemberInput
from src.database import Base, engine
from src.users.users_service import UserService
from test.users.conftest import fake, user_with_both, user_with_email, user_with_phone_number
from .test_init import client



@pytest.fixture(scope="session")
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
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    


@pytest.fixture
def mock_user():
    """
    Mock a user with email, phone number or both
    customer_type: IdentifierEnum The type of identifier to mock
    role: UserRole The role of the user
    """
    def _mock_user(customer_type: IdentifierEnum = None, role: UserRole = UserRole.CUSTOMER):
        result_payload = {}
        match (customer_type):
            case IdentifierEnum.PHONE_NUMBER:
                result_payload = {
                    **user_with_phone_number,
                    "role": role.value,
                }
            case IdentifierEnum.EMAIL:
                result_payload = {
                    **user_with_email,
                    "role": role.value,
                }
            case None:
                result_payload ={
                    **user_with_both,
                    "role": role.value,
                }
        return result_payload
    return _mock_user


@pytest.fixture
def create_user(get_test_db_session):
    """
    Create users in the test database
    user_data: dict The user data
    """
    def _create_user(user_data,is_member=False):
        if is_member:
            user = UserService(get_test_db_session).create(user_create_input=UserCreateMemberInput(**user_data))
        else:
            user = UserService(get_test_db_session).create(user_create_input=UserCreateInput(**user_data))
        return user
    return _create_user


@pytest.fixture(scope="session")
def generate_user_data():
    def _generate_user_data(role: UserRole = None, with_email=True, with_phone_number=True):
        return {
            "id": str(uuid.uuid4()),
            "email":  fake.unique.email() if with_email else None,
            "phone_number":  f"+22997{fake.random_number(digits=6, fix_len=True)}" if with_phone_number else None,
            "last_name": fake.last_name(),
            "first_name": fake.first_name(),
            "address": fake.address(),
            "password": "string",
            "phone_number_verification_code": str(fake.random_number(digits=6)),
            "phone_number_verification_expiry": str(datetime.now() + timedelta(days=1)),
            "email_verification_expiry": str(datetime.now() + timedelta(days=1)),
            "email_verification_code": str(fake.random_number(digits=6)),
            "reset_password_code": str(fake.random_number(digits=6)),
            "role":  role.value if role else fake.random_element(elements=[role.value for role in UserRole]),
            "phone_number_verified": fake.random_element(elements=[0, 1]),
            "email_verified": fake.random_element(elements=[0, 1])
        }
    return _generate_user_data
