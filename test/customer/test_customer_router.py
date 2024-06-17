
from ..test_init import client
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing_extensions import Annotated
from .mock_customer import mock_customer_with_email,mock_customer_with_phone_number, mock_verify_identifier_input, mock_reset_and_validation_input, mock_change_password_input, mock_submit_reset_password_input


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
AccessTokenDep = Annotated[str, Depends(oauth2_scheme)]


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

    def test_edit_customer(self,mock_edit_customer, access_token: AccessTokenDep):
        response = client.patch("/customers", json=mock_customer_with_phone_number, headers={"Authorization": f"Bearer {access_token}"});

        response_payload = response.json()

        assert response.status_code == 200, "User with phone number edited successfully"
        assert "id" in response_payload

    def test_verify_verification_code(self):
        response = client.post("/customers/verify_verification_code", json=mock_verify_identifier_input)
        response_payload = response.json()
        
        assert response.status_code == 200, "Verification code verified successfully"
        assert response_payload["verification_status"] == "verified"

    def test_generate_new_email_validation_code(self):
        response = client.post("/customers/send_verification_code", json=mock_reset_and_validation_input)
        response_payload = response.json()
        
        assert response.status_code == 200, "New validation code generated successfully"
        assert response_payload["code_sent"] == True

    def test_change_password(self):
        user_online = "mock_user_online"  # Mock a valid user online
        response = client.patch(
            "/customers/change_password",
            json=mock_change_password_input,
            headers={"Authorization": f"Bearer {user_online}"}
        )
        response_payload = response.json()
        
        assert response.status_code == 200, "Password changed successfully"
        assert response_payload["password_changed"] == True

    def test_reset_password(self):
        identifier = "mock_identifier"  # Mock a valid identifier
        response = client.patch(f"/customers/reset_password?identifier={identifier}")
        response_payload = response.json()
        
        assert response.status_code == 200, "Password reset successfully"
        assert response_payload["reset"] == True

    def test_submit_reset_password(self):
        response = client.patch("/customers/submit_reset_password", json=mock_submit_reset_password_input)
        response_payload = response.json()
        
        assert response.status_code == 200, "Password submitted successfully"
        assert response_payload["password_reset"] == True