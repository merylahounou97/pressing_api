
import sqlalchemy.orm

from test.customer.mock_customer import mock_customer_with_email, mock_customer_with_phone_number 
from .conftest import get_customer_by_identifier


from ..test_init import client


class TestCustomerRouter:
    def test_create_customer(
        self, mock_customer_with_email, mock_customer_with_phone_number
    ):
        response = client.post(
            "/customers?redirect_url=google.com", json=mock_customer_with_email
        )
        response_payload = response.json()
        # Create user with phone number
        assert (
            response.status_code == 200
        ), "User with phone number created successfully"
        assert response_payload["email_verified"] == False
        assert response_payload["email"] is not None

        response = client.post(
            "/customers?redirect_url=google.com", json=mock_customer_with_phone_number
        )
        response_payload = response.json()
        assert response.status_code == 200, "User with email created successfully"
        assert response_payload["phone_number_verified"] == False
        assert response_payload["phone_number"] is not None

    def test_verify_verification_code(
        self,get_customer_by_identifier_fix , mock_customer_with_email, mock_customer_with_phone_number
    ):
        user_created = get_customer_by_identifier_fix(mock_customer_with_email["email"])
        response = client.post(
            "/customers/verify_verification_code",
            json={
                "identifier": user_created.email,
                "verification_code": user_created.email_verification_code,
            },
        )
        response_payload = response.json()
        assert response.status_code == 200, "Verification code verified failed"
        assert response_payload["email_verified"] == True

        user_created = get_customer_by_identifier_fix(mock_customer_with_phone_number["phone_number"])
        print(user_created)
        response = client.post(
            "/customers/verify_verification_code",
            json={
                "identifier": user_created.phone_number,
                "verification_code": user_created.phone_number_verification_code,
            },
        )
        response_payload = response.json()
        assert response.status_code == 200, "Verification code verified failed"
        assert response_payload["phone_number_verified"] == True

    # def test_edit_customer(self, access_token):
    #     edit_input = {
    #         "first_name": "first_name modified",
    #         "last_name": "last_name modified",
    #         "address": "address modified",
    #         "email": "ahounoumeryl@yahoo.fr",
    #         "phone_number": {
    #             "iso_code": "string",
    #             "dial_code": "string",
    #             "phone_text": "+33751569562",
    #         },
    #         "email_redirect_url": "http://localhost",
    #     }
    #     response = client.patch(
    #         "/customers",
    #         json=edit_input,
    #         headers={"Authorization": f"Bearer {access_token}"},
    #     )

    #     response_payload = response.json()
    #     assert response.status_code == 200, "User with phone number edited successfully"
    #     assert "id" in response_payload
    #     assert response_payload["first_name"] == edit_input["first_name"]
    #     assert response_payload["last_name"] == edit_input["last_name"]
    #     assert response_payload["address"] == edit_input["address"]
    #     assert response_payload["email"] == edit_input["email"]
    #     assert response_payload["phone_number"] == edit_input["phone_number"]
    #     assert response_payload["email_verified"] == False
        assert response_payload["phone_number_verified"] == False

    # def test_send_verification_code(self):
    #     response = client.post("/customers/send_verification_code", json=mock_reset_and_validation_input)
    #     response_payload = response.json()

    #     assert response.status_code == 200, "New validation code generated successfully"


"""
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
        assert response_payload["password_reset"] == True"""
