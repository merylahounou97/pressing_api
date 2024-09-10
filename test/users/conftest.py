
from datetime import datetime, timedelta
import uuid
import pytest
from faker import Faker
from sqlalchemy import or_

from src.users.users_model import UserModel, UserRole
from src.users.users_service import UserService
from test.users.users_test_service import UserTestService
from passlib.hash import bcrypt
from test.test_init  import client


fake = Faker()


@pytest.fixture(scope="session")
def generate_user_data():
    def _generate_user_data(role: UserRole = None, with_email=True,
                            with_phone_number=True, email_verified=False, phone_number_verified=False):
        return {
            "id": str(uuid.uuid4()),
            "email":  fake.unique.email() if with_email else None,
            "phone_number":  f"+22997{fake.random_number(digits=6, fix_len=True)}" if with_phone_number else None,
            "last_name": fake.last_name(),
            "first_name": fake.first_name(),
            "address": fake.address(),
            "password": bcrypt.hash("string"),
            "phone_number_verification_code": str(fake.random_number(digits=6)),
            "phone_number_verification_expiry": str(datetime.now() + timedelta(days=1)),
            "email_verification_expiry": str(datetime.now() + timedelta(days=1)),
            "email_verification_code": str(fake.random_number(digits=6)),
            "reset_password_code": str(fake.random_number(digits=6)),
            "role":  role.value if role else fake.random_element(elements=[role.value for role in UserRole]),
            "phone_number_verified": phone_number_verified,
            "email_verified": email_verified

        }
    return _generate_user_data



@pytest.fixture
def get_access_token():
    """Fixture pour récupérer un token d'accès"""

    def _access_token(
        identifier,
        password,
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


user_with_email = {
    "last_name": "Aiounou",
    "first_name": "Ulrich",
    "address": "string",
    "email": "aiounouu@gmail.com",
    "password": "string",
}

user_with_both = {
    "last_name": "Ahounou",
    "first_name": "Méryl",
    "address": "string",
    "phone_number": "+22966086304",
    "email": "aiounoud@yahoo.fr",
    "password": "string",
}

user_with_phone_number = {
    "last_name": "Ahounou",
    "first_name": "Méryl",
    "address": "string",
    "phone_number": "+33666495244",
    "password": "string",
}


@pytest.fixture
def get_user_no_verified_phone_number(get_test_db_session):
    def _get_user_no_verified_phone_number():
        return (
            get_test_db_session.query(UserModel)
            .filter(UserModel.phone_number_verified == False)
            .populate_existing()
            .first()
        )
    return _get_user_no_verified_phone_number


@pytest.fixture
def get_user_no_verified_email(get_test_db_session):

    def _get_user_no_verified_email():
        return (
            get_test_db_session.query(UserModel)
            .filter(UserModel.email_verified == False)
            .populate_existing()
            .first()
        )
    return _get_user_no_verified_email


@pytest.fixture
def get_user_by_identifier(get_test_db_session):
    """
    Get a user by identifier in the test database
    identifier: str The identifier of the user
    """
    def _get_user_by_identifier(identifier: str) -> UserModel:
        return (
            get_test_db_session.query(UserModel)
            .filter(
                or_(
                    UserModel.phone_number == identifier,
                    UserModel.email == identifier,
                )
            )
            .populate_existing()
            .first()
        )

    return _get_user_by_identifier


@pytest.fixture(scope="class")
def mock_users_service(request, mock_db_session):
    """ This fixture creates a user service mock and injects it into the test class"""
    request.cls.users_service = UserService(mock_db_session)


@pytest.fixture
def user_test_service(generate_user_data, get_user_no_verified_email, get_user_no_verified_phone_number, get_user_by_identifier, get_users_data, get_random_user, get_all_users):
    return UserTestService(generate_user_data, get_user_no_verified_email, get_user_no_verified_phone_number, get_user_by_identifier, get_users_data, get_random_user, get_all_users)


@pytest.fixture(scope="session")
def get_users_data(generate_user_data):
    def _get_users_data():
        return [generate_user_data() for _ in range(3)]
    return _get_users_data


@pytest.fixture
def get_random_user(get_test_db_session):
    def _get_random_user():
        return get_test_db_session.query(UserModel).first()
    return _get_random_user
