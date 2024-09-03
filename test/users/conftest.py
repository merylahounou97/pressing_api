
import pytest
from faker import Faker
from sqlalchemy import or_

from src.users.users_model import UserModel
from src.users.users_service import UserService
from test.users.users_test_service import UserTestService


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
    def _get_user_by_identifier(identifier: str)-> UserModel:
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




fake = Faker()

@pytest.fixture(scope="class")
def mock_users_service(request, mock_db_session):
    """ This fixture creates a user service mock and injects it into the test class"""
    request.cls.users_service = UserService(mock_db_session)

@pytest.fixture
def user_test_service(generate_user_data, create_user, get_access_token,get_user_no_verified_email,get_user_no_verified_phone_number,get_user_by_identifier,get_users_data,get_random_user):
    return UserTestService(generate_user_data, create_user, get_access_token,get_user_no_verified_email,get_user_no_verified_phone_number,get_user_by_identifier,get_users_data,get_random_user)

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