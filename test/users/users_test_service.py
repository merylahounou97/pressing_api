from src.users.users_model import UserModel
from src.users.users_schemas import UserOutput
from src.utils.constants import Constants
from src.utils.error_messages import ErrorMessages
from test.base_test_service import BaseTestService


class UserTestService(BaseTestService):
    base_url = f"/{Constants.USERS}"

    def __init__(
        self,
        generate_user_data,
        get_user_by_identifier,
        get_all_users,
        get_access_token,
        get_all_admins,
        get_all_secretaries,
    ):
        self.get_user_by_identifier = get_user_by_identifier
        self.generate_user_data = generate_user_data
        self.all_users = get_all_users
        self.password = "string"
        self.updated_password = "new_password"
        self.get_access_token = get_access_token
        self.admins = get_all_admins
        self.secretaries = get_all_secretaries

    def create_user_with_email_only(self):
        """Create a user with email only and make post request for its creation"""
        user = self.generate_user_data()
        user["phone_number"] = None
        user["phone_number_verified"] = 0
        response_payload = self.request_create_user(user)
        assert response_payload.email_verified is False
        assert response_payload.email is not None

    def create_user_with_phone_number_and_email(self):
        """Create a user with phone number and email and make post request for its creation"""
        user = {
            **self.generate_user_data(),
            "email_verified": 0,
            "phone_number_verified": 0,
        }
        response_payload = self.request_create_user(user)
        assert response_payload.phone_number_verified is False
        assert response_payload.email_verified is False
        assert response_payload.email is not None
        assert response_payload.phone_number is not None

    def create_user_with_phone_number_only(self):
        """Create a user with phone number only and make post request for its creation"""
        user = {**self.generate_user_data(), "phone_number_verified": 0, "email": None}
        response_payload = self.request_create_user(user)
        assert response_payload.phone_number_verified is False
        assert response_payload.phone_number is not None

    def request_verify_verification_code_email(self):
        """Make a request to verify the email verification code"""

        # Get the user form database so that we can get the verification code
        user_created = self.get_user_by_identifier(self.all_users[0]["email"])
        response = self.client.post(
            f"{self.base_url}/verify_verification_code",
            json={
                "identifier": user_created.email,
                "verification_code": user_created.email_verification_code,
            },
        )
        assert response.status_code == 200, "Verification code verified failed"
        response_payload = UserModel(**response.json())
        assert response_payload.email_verified is True

    def request_verify_verification_code_phone_number(self):
        """Make a request to verify the phone number verification code"""

        # Get the user form database so that we can get the verification code
        user_created = self.get_user_by_identifier(self.all_users[0]["email"])
        response = self.client.post(
            f"{self.base_url}/verify_verification_code",
            json={
                "identifier": user_created.phone_number,
                "verification_code": user_created.phone_number_verification_code,
            },
        )
        assert response.status_code == 200, "Verification code verified failed"
        response_payload = UserModel(**response.json())
        assert response_payload.phone_number_verified is True

    def request_create_user(self, user):
        """Make a request to create a user"""
        response = self.client.post(self.base_url, json=user)
        response_payload = UserOutput(**response.json())
        # Create user with phone number
        assert (
            response.status_code == 200
        ), "User with phone number created successfully"

        return response_payload

    def sent_verification_code_for_email(self):
        """Send verification code for email"""

        user = self.all_users[1]
        response = self.client.post(
            f"{self.base_url}/send_verification_code",
            json={"identifier": user["email"]},
        )
        assert response.status_code == 200, "Failed to send email verification"

        # Get the email verification code before the request
        old_code = user["email_verification_code"]
        # Get the user form database so that we can compare the verification code
        user = self.get_user_by_identifier(user["email"])
        assert old_code != user.email_verification_code, "Code are the same"
        assert not user.email_verified, "Email verification should be false"

    def sent_verification_code_for_phone_number(self):
        """Send verification code for phone number"""

        user = self.all_users[1]
        old_code = user["phone_number_verification_code"]
        response = self.client.post(
            f"{self.base_url}/send_verification_code",
            json={"identifier": user["phone_number"]},
        )

        user = self.get_user_by_identifier(user["phone_number"])

        assert response.status_code == 200, "Failed to send phone number verification"
        assert old_code != user.phone_number_verification_code, "Code are the same"
        assert (
            not user.phone_number_verified
        ), "Phone number verification should be false"

    def change_password(self):
        user = self.all_users[2]
        access_token = self.get_access_token(user["email"], self.password)

        # Cannot change password with old password
        response = self.client.patch(
            f"{self.base_url}/change_password",
            json={"old_password": self.password, "new_password": self.password},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 400, "Password changed Failed"
        assert (
            response.json()["detail"] == ErrorMessages.NEW_PASSWORD_SAME_AS_OLD
        ), "NEW_PASSWORD_SAME_AS_OLD error message not returned"

        # Change password with wrong old password
        response = self.client.patch(
            f"{self.base_url}/change_password",
            json={
                "old_password": "false_password",
                "new_password": self.updated_password,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 400, "Password changed Failed"
        assert (
            response.json()["detail"] == ErrorMessages.WRONG_OLD_PASSWORD
        ), "Wrong password error message not returned"

        # Change password with new password
        response = self.client.patch(
            f"{self.base_url}/change_password",
            json={
                "old_password": self.password,
                "new_password": self.updated_password,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200, "Password not changed"
        new_access_token = self.get_access_token(user["email"], self.updated_password)
        assert new_access_token is not None, "Access token not returned"

        # Cannot change password of users with email not verified
        user = self.all_users[1]
        # We first relog the user to get the new access token
        access_token = self.get_access_token(
            user["email"],
            self.password,
        )
        response = self.client.patch(
            f"{self.base_url}/change_password",
            json={
                "old_password": self.password,
                "new_password": self.updated_password,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 400, "Password changed Failed"
        assert (
            response.json()["detail"]
            == ErrorMessages.EMAIL_OR_PHONE_NUMBER_VERIFICATION_REQUIRED
        ), "Email not verified error message not returned"

    def reset_password(self):
        user = self.all_users[2]
        response = self.client.patch(
            f"{self.base_url}/reset_password",
            json={"identifier": user["email"]},
        )
        assert response.status_code == 200, "Reset password failed"

        user = self.admins[0]
        response = self.client.patch(
            f"{self.base_url}/reset_password",
            json={"identifier": user["phone_number"]},
        )
        assert response.status_code == 200, "Reset password failed"

    def submit_reset_password_with_email(self):
        user = self.all_users[0]
        response = self.client.patch(
            f"{self.base_url}/submit_reset_password",
            json={
                "identifier": user["email"],
                "verification_code": user["reset_password_code"],
                "new_password": self.updated_password,
            },
        )
        assert response.status_code == 200, "Reset password failed"

        access_token = self.get_access_token(user["email"], self.updated_password)
        assert access_token is not None, "Access token not returned"

    def submit_reset_password_with_phone_number(self):
        user = self.all_users[1]
        response = self.client.post(
            f"{self.base_url}/submit_reset_password",
            json={
                "identifier": user["phone_number"],
                "phone_number_verification_code": user[
                    "phone_number_verification_code"
                ],
                "new_password": self.updated_password,
            },
        )
        assert response.status_code == 200, "Reset password failed"

        access_token = self.get_access_token(
            user["phone_number"], self.updated_password
        )
        assert access_token is not None, "Access token not returned"

    def edit_user(self):
        """Test edit user with first name, last name, address, email, phone number and email redirect url"""
        user = self.all_users[2]
        access_token = self.get_access_token(user["email"], self.updated_password)

        edit_input = {
            "first_name": "first_name modified",
            "last_name": "last_name modified",
            "address": "address modified",
            "email": "test@yahoo.fr",
            "phone_number": "+33758959563",
        }
        response = self.client.patch(
            self.base_url,
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

    def get_all_users(self):
        """Test get all users"""

        # Try to get all users without being logged in as admin or secretary
        user = self.all_users[0]
        access_token = self.get_access_token(user["email"], self.updated_password)
        response = self.client.get(
            self.base_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        assert (
            response.status_code == 401
        ), "A non admin or secretary should not be able to get all users"

        # Try to get all users as a secretary
        secretary = self.secretaries[0]
        secretary_access_token = self.get_access_token(
            secretary["email"], self.password
        )
        response = self.client.get(
            self.base_url, headers={"Authorization": f"Bearer {secretary_access_token}"}
        )
        assert response.status_code == 200, "Secretary should be able to get all users"
        assert isinstance(response.json(), list), "Return should be a list of users"

        # # Try to get all users as an admin
        admin = self.admins[0]
        admin_access_token = self.get_access_token(admin["email"], self.password)
        response = self.client.get(
            self.base_url, headers={"Authorization": f"Bearer {admin_access_token}"}
        )
        assert response.status_code == 200, "Admin should be able to get all users"
        assert isinstance(response.json(), list), "Return should be a list of users"

        # Try to get a user with a specific criteria
        response = self.client.get(
            self.base_url,
            params={"first_name": secretary["first_name"]},
            headers={"Authorization": f"Bearer {admin_access_token}"},
        )
        assert (
            response.status_code == 200
        ), "Admin should be able to get all users with a specific criteria"
        response_payload = response.json()
        assert isinstance(response_payload, list), "Return should be a list of users"
        filter_response = filter(
            lambda user: user["first_name"] == secretary["first_name"], response_payload
        )
        assert len(list(filter_response)) == len(
            response_payload
        ), "The user with the specific criteria should be in the list"
