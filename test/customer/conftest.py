import pytest
from sqlalchemy import or_
from src.customer.customer_model import CustomerModel
from src.dependencies.get_customer_online import get_customer_online
from src.person.person_schema import IdentifierEnum
import uuid


@pytest.fixture
def get_customer_by_identifier_fix(get_test_db_session):
    def _get_customer_by_identifier(identifier: str):
        return get_test_db_session.query(CustomerModel).filter(
            or_(CustomerModel.phone_number==identifier,CustomerModel.email==identifier)
            ).populate_existing().first() 

    return _get_customer_by_identifier

@pytest.fixture
def get_customer_online_fix(get_test_db_session):
    def _get_customer_online(access_token):
        return get_customer_online(access_token=access_token, db=get_test_db_session)
    return _get_customer_online


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
def mock_customer_with_both():
    return {
        "last_name": "Ahounou",
        "first_name": "Méryl",
        "address": "string",
        "phone_number":"+22966086304",
        "email": "aiounoud@yahoo.fr",
        "password": "string",
    }

@pytest.fixture
def mock_customer_with_phone_number():
    return {
        "last_name": "Ahounou",
        "first_name": "Méryl",
        "address": "string",
        "phone_number": "+33666495244",
        "password": "string",
    }

@pytest.fixture
def mock_customer(mock_customer_with_email
                  ,mock_customer_with_phone_number
                  ,mock_customer_with_both
                  ):
    def _mock_customer(customer_type: IdentifierEnum=None):
        match(customer_type):
            case IdentifierEnum.PHONE_NUMBER:
                return mock_customer_with_phone_number
            case IdentifierEnum.EMAIL:
                return mock_customer_with_email
            case None:
                return mock_customer_with_both
    return _mock_customer
