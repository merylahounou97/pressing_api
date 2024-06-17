import pytest
from src.customer.customer_model import CustomerModel


@pytest.fixture
def mock_customer_with_phone_number():
    return {
        "last_name": "Ahounou",
        "first_name": "Méryl",
        "address": "string",
        "phone_number": {
            "iso_code": "string",
            "dial_code": "string",
            "phone_text": "+33666495244",
        },
        "password": "string",
    }


@pytest.fixture
def mock_customer_with_email():
    return {
        "last_name": "Aiounou",
        "first_name": "Ulrich",
        "address": "string",
        "email": "aiounouu@gmail.com",
        "password": "string",
    }


@pytest.fixture
def mock_edit_customer():
    return {
        "first_name": "Thomas",
    }


@pytest.fixture
def mock_verify_identifier_input():
    return {"identifier": "ahounoumeryl@yahoo.fr", "code": "123456"}


@pytest.fixture
def mock_reset_and_validation_input():
    return {"identifier": "ahounoumeryl@yahoo.fr"}


@pytest.fixture
def mock_change_password_input():
    return {"old_password": "oldpassword", "new_password": "newpassword"}


@pytest.fixture
def mock_reset_password_input():
    return {"identifier": "ahounoumeryl@yahoo.fr"}


@pytest.fixture
def mock_submit_reset_password_input():
    return {
        "identifier": "ahounoumeryl@yahoo.fr",
        "new_password": "newpassword",
        "code": "123456",
    }


@pytest.fixture
def mock_customer_model(mock_customer_with_phone_number):
    return CustomerModel(**mock_customer_with_phone_number())
