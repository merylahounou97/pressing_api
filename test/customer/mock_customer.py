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
    "phone_text": "+33 6 66 49 52 44"
  },
  "password": "string"
}

@pytest.fixture
def mock_customer_with_email():
    return {
  "last_name": "Aiounou",
  "first_name": "Ulrich",
  "address": "string",
  "email": "aiounouu@gmail.com",
  "password": "string"
}

@pytest.fixture
def mock_customer_model(mock_customer_with_phone_number):
    return CustomerModel(**mock_customer_with_phone_number())