from test.test_init import client


from src.users.users_model import UserRole
from src.users.users_schemas import IdentifierEnum, UserOutput, UserQueryOptions
from src.utils.error_messages import ErrorMessages
from src.utils.constants import Constants

BASE_URL = f"/{Constants.USERS}"


class TestUsersRouter:
    """Test the user router"""

    updated_password = "new_secure_password"
    
    def test_create_user(self, user_test_service):
        """
        Test create user with email, phone number and both
        """
        user_test_service.create_user_with_email_only()

        user_test_service.create_user_with_phone_number_only()

        user_test_service.create_user_with_phone_number_and_email()

    def test_verify_verification_code(
        self, user_test_service
    ):
        """
        Test verify verification code with email and phone number
        """

        user_test_service.request_verify_verification_code_email()
        user_test_service.request_verify_verification_code_phone_number()

    def test_send_verification_code(
            self, user_test_service):
        """
        Test send verification code with email and phone number
        """
        user_test_service.sent_verification_code_for_email()
        user_test_service.sent_verification_code_for_phone_number()

    # def test_change_password(self, get_access_token, mock_user,user_test_service):
    #     """ Test change password with old password and new password"""

    #     user = mock_user()

    #     access_token = get_access_token(user["email"], user["password"])

    #     # Cannot change password with old password
    #     response = client.patch(
    #         f"{BASE_URL}/change_password",
    #         json={
    #             "old_password": user["password"],
    #             "new_password": user["password"],
    #         },
    #         headers={"Authorization": f"Bearer {access_token}"},
    #     )
    #     assert response.status_code == 400, "Password changed Failed"
    #     assert (
    #         response.json()["detail"] == ErrorMessages.NEW_PASSWORD_SAME_AS_OLD
    #     ), "NEW_PASSWORD_SAME_AS_OLD error message not returned"

    #     # Change password with new password
    #     response = client.patch(
    #         f"{BASE_URL}/change_password",
    #         json={
    #             "old_password": user["password"],
    #             "new_password": self.updated_password,
    #         },
    #         headers={"Authorization": f"Bearer {access_token}"},
    #     )

    #     assert response.status_code == 200, "Password not changed"
    #     new_access_token = get_access_token(
    #         user["email"], self.updated_password)
    #     assert new_access_token is not None, "Access token not returned"

    #     # Cannot change password with wrong old password
    #     response = client.patch(
    #         f"{BASE_URL}/change_password",
    #         json={
    #             "old_password": user["password"],
    #             "new_password": self.updated_password,
    #         },
    #         headers={"Authorization": f"Bearer {access_token}"},
    #     )

    #     assert response.status_code == 400, "Password changed Failed"
    #     assert (
    #         response.json()["detail"] == ErrorMessages.WRONG_OLD_PASSWORD
    #     ), "Wrong password error message not returned"

    #     # Cannot change password with wrong old password
    #     user_with_email_not_verified = mock_user(IdentifierEnum.EMAIL)
    #     # We first relog the user to get the new access token
    #     access_token = get_access_token(
    #         user_with_email_not_verified["email"],
    #         user_with_email_not_verified["password"],
    #     )
    #     response = client.patch(
    #         f"{BASE_URL}/change_password",
    #         json={
    #             "old_password": user_with_email_not_verified["password"],
    #             "new_password": self.updated_password,
    #         },
    #         headers={"Authorization": f"Bearer {access_token}"},
    #     )

    #     assert response.status_code == 400, "Password changed Failed"
    #     assert (
    #         response.json()["detail"]
    #         == ErrorMessages.EMAIL_OR_PHONE_NUMBER_VERIFICATION_REQUIRED
    #     ), "Email not verified error message not returned"

    # # def test_reset_password(self, mock_user):
    # #     """Test reset password with email and phone number"""
    # #     # For email address
    # #     identifier = mock_user(IdentifierEnum.EMAIL)["email"]
    # #     response = client.patch(
    # #         f"{BASE_URL}/reset_password", json={"identifier": identifier})

    # #     assert response.status_code == 200, "Failed to send the code via email"

    # #     # For phone number
    # #     identifier = mock_user(IdentifierEnum.PHONE_NUMBER)["phone_number"]
    # #     response = client.patch(
    # #         f"{BASE_URL}/reset_password", json={"identifier": identifier})

    # #     assert response.status_code == 200, "Failed to send the code via phone number"

    # # def test_submit_reset_password(self, get_user_by_identifier, mock_user, get_access_token):
    # #     """Test submit reset password with email and phone number"""

    # #     # For email address
    # #     identifier = mock_user(IdentifierEnum.EMAIL)["email"]
    # #     user_created = get_user_by_identifier(identifier)
    # #     data = {
    # #         "identifier": identifier,
    # #         "verification_code": user_created.reset_password_code,
    # #         "new_password": mock_user(IdentifierEnum.EMAIL)["password"]
    # #     }
    # #     response = client.patch(f"{BASE_URL}/submit_reset_password", json=data)

    # #     assert response.status_code == 200, "Password not submitted successfully via email"

    # #     access_token = get_access_token(identifier, data["new_password"])

    # #     assert access_token is not None, "Access token not returned"

    # #     # For phone number
    # #     identifier = mock_user(IdentifierEnum.PHONE_NUMBER)["phone_number"]
    # #     user_created = get_user_by_identifier(identifier)
    # #     data = {
    # #         "identifier": identifier,
    # #         "verification_code": user_created.reset_password_code,
    # #         "new_password": mock_user(IdentifierEnum.PHONE_NUMBER)["password"]
    # #     }
    # #     response = client.patch(f"{BASE_URL}/submit_reset_password", json=data)

    # #     assert response.status_code == 200, "Password not submitted successfully via phone_number"

    # #     access_token = get_access_token(identifier, data["new_password"])

    # #     assert access_token is not None, "Access token not returned"

    # # def test_edit_user(self, get_access_token, mock_user):
    # #     """Test edit user with first name, last name, address, email, phone number and email redirect url"""
    # #     access_token = get_access_token(
    # #         mock_user()["email"], self.updated_password
    # #     )
    # #     edit_input = {
    # #         "first_name": "first_name modified",
    # #         "last_name": "last_name modified",
    # #         "address": "address modified",
    # #         "email": "ahounoumeryl@yahoo.fr",
    # #         "phone_number": "+33751569562",
    # #     }
    # #     response = client.patch(
    # #         f"{BASE_URL}",
    # #         json=edit_input,
    # #         headers={"Authorization": f"Bearer {access_token}"},
    # #     )
    # #     response_payload = response.json()
    # #     assert response.status_code == 200, "modification failed"
    # #     assert "id" in response_payload
    # #     assert response_payload["first_name"] == edit_input["first_name"]
    # #     assert response_payload["last_name"] == edit_input["last_name"]
    # #     assert response_payload["address"] == edit_input["address"]
    # #     assert response_payload["email"] == edit_input["email"]
    # #     assert response_payload["phone_number"] == edit_input["phone_number"]
    # #     assert response_payload["email_verified"] is False
    # #     assert response_payload["phone_number_verified"] is False

    # # def test_get_all_users(self, get_access_token, generate_user_data, create_user):
    # #     """Test get all users"""

    # #     # Try to get all users without being logged in as admin or secretary
    # #     access_token = get_access_token()
    # #     response = client.get(
    # #         BASE_URL, headers={"Authorization": f"Bearer {access_token}"})
    # #     assert response.status_code == 401, "A non admin or secretary should not be able to get all users"

    # #     # Try to get all users as a secretary
    # #     secretary_data = generate_user_data(role=UserRole.SECRETARY)
    # #     # Create the secretary
    # #     secretary = create_user(secretary_data, is_member=True)
    # #     secretary_access_token = get_access_token(
    # #         secretary.email, secretary_data["password"])
    # #     response = client.get(
    # #         BASE_URL, headers={"Authorization": f"Bearer {secretary_access_token}"})
    # #     assert response.status_code == 200, "Secretary should be able to get all users"
    # #     assert isinstance(
    # #         response.json(), list), "Return should be a list of users"

    # #     # Try to get all users as an admin
    # #     admin_data = generate_user_data(role=UserRole.ADMIN)
    # #     # Create the admin
    # #     admin = create_user(admin_data, is_member=True)
    # #     admin_access_token = get_access_token(
    # #         admin.email, admin_data["password"])
    # #     response = client.get(
    # #         BASE_URL, headers={"Authorization": f"Bearer {admin_access_token}"})
    # #     assert response.status_code == 200, "Admin should be able to get all users"
    # #     assert isinstance(
    # #         response.json(), list), "Return should be a list of users"

    # #     # Try to get a user with a specific criteria
    # #     response = client.get(BASE_URL, params={"first_name": secretary.first_name},
    # #                           headers={"Authorization": f"Bearer {admin_access_token}"})
    # #     assert response.status_code == 200, "Admin should be able to get all users with a specific criteria"
    # #     response_payload = response.json()
    # #     assert isinstance(response_payload,
    # #                       list), "Return should be a list of users"
    # #     filter_response = filter(
    # #         lambda user: user["first_name"] == secretary.first_name, response_payload)
    # #     assert len(list(filter_response)) == len(
    # #         response_payload), "The user with the specific criteria should be in the list"
