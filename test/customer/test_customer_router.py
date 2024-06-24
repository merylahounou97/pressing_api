from http.client import HTTPException
import pytest
from src.person.person_schema import IdentifierEnum
from src.utils.error_messages import ErrorMessages

from ..test_init import client


class TestCustomerRouter:
    updated_password = "new_secure_password"

    def test_create_customer(self, mock_customer):
        data = mock_customer(IdentifierEnum.EMAIL)
        response = client.post("/customers?redirect_url=google.com", json=data)
        response_payload = response.json()
        # Create user with phone number
        assert (
            response.status_code == 200
        ), "User with phone number created successfully"
        assert response_payload["email_verified"] is False
        assert response_payload["email"] is not None

        data = mock_customer(IdentifierEnum.PHONE_NUMBER)
        response = client.post("/customers?redirect_url=google.com", json=data)
        response_payload = response.json()
        assert response.status_code == 200, "User with email created successfully"
        assert response_payload["phone_number_verified"] is False
        assert response_payload["phone_number"] is not None

        response = client.post(
            "/customers?redirect_url=google.com", json=mock_customer()
        )
        response_payload = response.json()
        assert (
            response.status_code == 200
        ), "user with both email and phone number not created"
        assert response_payload["phone_number_verified"] is False
        assert response_payload["phone_number"] is not None
        assert response_payload["email_verified"] is False
        assert response_payload["email"] is not None

    def test_verify_verification_code(
        self, get_customer_by_identifier_fix, mock_customer
    ):
        identifier = mock_customer()["email"]
        user_created = get_customer_by_identifier_fix(identifier)
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

        identifier = mock_customer()["phone_number"]

        user_created = get_customer_by_identifier_fix(identifier)
        response = client.post(
            "/customers/verify_verification_code",
            json={
                "identifier": user_created.phone_number,
                "verification_code": user_created.phone_number_verification_code,
            },
        )
        response_payload = response.json()
        assert response.status_code == 200, "Verification code verified failed"
        assert response_payload["phone_number_verified"] is True

    def test_send_verification_code(
        self, get_customer_by_identifier_fix, mock_customer
    ):
        # For email address
        idenfifier = mock_customer(IdentifierEnum.EMAIL)["email"]
        user = get_customer_by_identifier_fix(idenfifier)

        old_code = user.email_verification_code
        response = client.post(
            "/customers/send_verification_code", json={"identifier": idenfifier}
        )
        assert response.status_code == 200, "Failed to send email verification"

        user = get_customer_by_identifier_fix(idenfifier)

        assert old_code != user.email_verification_code, "Code are the same"
        assert user.email_verified == 0, "Email verification should be false"

        # For phone number
        idenfifier = mock_customer(IdentifierEnum.PHONE_NUMBER)["phone_number"]
        user = get_customer_by_identifier_fix(idenfifier)
        old_code = user.phone_number_verification_code

        response = client.post(
            "/customers/send_verification_code", json={"identifier": idenfifier}
        )

        assert response.status_code == 200, "Failed to send phone number verification"

        user = get_customer_by_identifier_fix(idenfifier)
        assert old_code != user.phone_number_verification_code, "Code are the same"
        assert (
            user.phone_number_verified == 0
        ), "Phone number verification should be false"

    def test_change_password(self, get_access_token, mock_customer):
        user = mock_customer()
        access_token = get_access_token(user["email"], user["password"])

        # Cannot change password with old password
        response = client.patch(
            "/customers/change_password",
            json={
                "old_password": user["password"],
                "new_password": user["password"],
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 400, "Password changed Failed"
        assert (
            response.json()["detail"] == ErrorMessages.NEW_PASSWORD_SAME_AS_OLD
        ), "NEW_PASSWORD_SAME_AS_OLD error message not returned"

        # Change password with new password
        response = client.patch(
            "/customers/change_password",
            json={
                "old_password": user["password"],
                "new_password": self.updated_password,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200, "Password not changed"
        new_access_token = get_access_token(user["email"], self.updated_password)
        assert new_access_token is not None, "Access token not returned"

        # Cannot change password with wrong old password
        response = client.patch(
            "/customers/change_password",
            json={
                "old_password": user["password"],
                "new_password": self.updated_password,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 400, "Password changed Failed"
        assert (
            response.json()["detail"] == ErrorMessages.WRONG_OLD_PASSWORD
        ), "Wrong password error message not returned"

        # Cannot change password with wrong old password
        user_with_email_not_verified = mock_customer(IdentifierEnum.EMAIL)
        # We first relog the user to get the new access token
        access_token = get_access_token(
            user_with_email_not_verified["email"],
            user_with_email_not_verified["password"],
        )
        response = client.patch(
            "/customers/change_password",
            json={
                "old_password": user_with_email_not_verified["password"],
                "new_password": self.updated_password,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 400, "Password changed Failed"
        assert (
            response.json()["detail"]
            == ErrorMessages.EMAIL_OR_PHONE_NUMBER_VERIFICATION_REQUIRED
        ), "Email not verified error message not returned"


    def test_reset_password(self, get_customer_by_identifier_fix, mock_customer):
        # For email address
        identifier = mock_customer(IdentifierEnum.EMAIL)["email"]
        
        response = client.patch(f"/customers/reset_password", json= {"identifier" : identifier})

        assert response.status_code == 200, "Failed to send the code via email"

        # For phone number
        identifier = mock_customer(IdentifierEnum.PHONE_NUMBER)["phone_number"]
        
        response = client.patch(f"/customers/reset_password", json= {"identifier" : identifier})


        assert response.status_code == 200, "Failed to send the code via phone number"


    def test_submit_reset_password(self, get_customer_by_identifier_fix, mock_customer, get_access_token):
        # For email address
        identifier =mock_customer(IdentifierEnum.EMAIL)["email"]
        user_created = get_customer_by_identifier_fix(identifier)
        data = {
        "identifier": identifier,
        "verification_code": user_created.reset_password_code,
        "new_password": mock_customer(IdentifierEnum.EMAIL)["password"]
    }
        response = client.patch("/customers/submit_reset_password", json=data)

        assert response.status_code == 200, "Password not submitted successfully via email"

        access_token = get_access_token(identifier, data["new_password"])

        assert access_token is not None, "Access token not returned"

        # For phone number
        identifier =mock_customer(IdentifierEnum.PHONE_NUMBER)["phone_number"]
        user_created = get_customer_by_identifier_fix(identifier)
        data = {
        "identifier": identifier,
        "verification_code": user_created.reset_password_code,
        "new_password": mock_customer(IdentifierEnum.PHONE_NUMBER)["password"]
    }
        response = client.patch("/customers/submit_reset_password", json=data)

        assert response.status_code == 200, "Password not submitted successfully via phone_number"

        access_token = get_access_token(identifier, data["new_password"])

        assert access_token is not None, "Access token not returned"



    def test_edit_customer(self, get_access_token, mock_customer_with_both):
        access_token = get_access_token(
            mock_customer_with_both["email"], self.updated_password
        )
        edit_input = {
            "first_name": "first_name modified",
            "last_name": "last_name modified",
            "address": "address modified",
            "email": "ahounoumeryl@yahoo.fr",
            "phone_number": "+33751569562",
            "email_redirect_url": "http://localhost",
        }

        response = client.patch(
            "/customers",
            json=edit_input,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        response_payload = response.json()
        assert response.status_code == 200, "modification failed"
        assert "id" in response_payload
        assert response_payload["first_name"] == edit_input["first_name"]
        assert response_payload["last_name"] == edit_input["last_name"]
        assert response_payload["address"] == edit_input["address"]
        assert response_payload["email"] == edit_input["email"]
        assert response_payload["phone_number"] == edit_input["phone_number"]
        assert response_payload["email_verified"] is False
        assert response_payload["phone_number_verified"] is False
