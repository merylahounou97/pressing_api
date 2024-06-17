import pytest
from sqlalchemy import or_
from src.customer.customer_model import CustomerModel
from src.customer.customer_service import get_customer_by_email_or_phone
from test.conftest import get_test_db_session


@pytest.fixture
def get_customer_by_identifier(get_test_db_session):
    def _get_customer_by_identifier(identifier: str):
        return get_customer_by_email_or_phone(
            get_test_db_session, identifier, identifier
        )

    return _get_customer_by_identifier
