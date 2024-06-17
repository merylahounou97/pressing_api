from src.customer import customer_service
from test.customer.mock_customer import (
    mock_customer_with_phone_number,
    mock_customer_with_email,
)
from ..conftest import mock_db_session


# class TestCustomerService:
#     def test_check_existing_customer(
#         self, mock_db_session, mock_customer_with_phone_number, mock_customer_with_email
#     ):
#         userBool = customer_service.check_existing_customer(
#             db=mock_db_session,
#             email=mock_customer_with_email["email"],
#             phone_number=mock_customer_with_phone_number["phone_number"],
#         )
#         assert userBool is True, "The user should not exist"
