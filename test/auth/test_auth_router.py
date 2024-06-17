import pytest

from test.customer.mock_customer import mock_customer_with_email

from ..test_init import client


class TestAuthRouter:
    pass

    # def test_login_customer(self,mock_customer_with_email):
    #     response = client.post("/token",data={
    #         "username": mock_customer_with_email["email"],
    #         "password": mock_customer_with_email["password"],
    #     }, headers={
    #         "Content-Type": "application/x-www-form-urlencoded",
    #         "Accept": "application/json"
    #     })
    #     response_payload = response.json()
    #     assert response.status_code == 200, "User with email logged in successfully"
    #     assert response_payload["access_token"] is not None, "Access token is provided"
    #     return response_payload["access_token"]
