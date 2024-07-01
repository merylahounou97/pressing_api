import uuid
from datetime import datetime, timedelta
from typing import List

import pytest
from faker import Faker
from sqlalchemy import or_

from src.users.users_model import UserModel, UserRole
from src.users.users_schemas import IdentifierEnum, UserCreateInput, UserCreateMemberInput
from src.users.users_service import UserService

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

@pytest.fixture
def generate_user_data():
    def _generate_user_data(role: UserRole = None):
        return {
            "id": str(uuid.uuid4()),
            "email": fake.unique.email(),
            "phone_number": f"+22997{fake.random_number(digits=6, fix_len=True)}",
            "last_name": fake.last_name(),
            "first_name": fake.first_name(),
            "address": fake.address(),
            "password": fake.password(),
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

@pytest.fixture(scope="class")
def mock_users_service(request, mock_db_session):
    """ This fixture creates a user service mock and injects it into the test class"""
    request.cls.users_service = UserService(mock_db_session)