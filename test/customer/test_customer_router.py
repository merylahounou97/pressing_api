
from ..test_init import client
from .mock_customer import mock_customer_with_email,mock_customer_with_phone_number


class TestCustomerRouter():
    def test_create_customer(self,mock_customer_with_email,
                            mock_customer_with_phone_number):
        response = client.post("/customers?redirect_url=google.com", json=mock_customer_with_phone_number);
        response_payload = response.json()
        
        #Create user with phone number
        assert response.status_code == 200, "User with phone number created successfully"
        assert response_payload["email_verified"] == False
        assert response_payload["phone_number_verified"] == False
        assert not (response_payload["email"] is None and response_payload["phone_number"]  is None)

        response = client.post("/customers?redirect_url=google.com", json=mock_customer_with_email)
        assert response.status_code == 200, "User with email created successfully"
