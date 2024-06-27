import pytest
from sqlalchemy import or_
from src.users.user_schemas import IdentifierEnum
from src.users.user_model import UserModel, UserRole

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