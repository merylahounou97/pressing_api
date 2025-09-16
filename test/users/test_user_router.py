from test.test_init import client


from src.users.users_model import UserRole
from src.users.users_schemas import IdentifierEnum, UserOutput, UserQueryOptions
from src.utils.error_messages import ErrorMessages
from src.utils.constants import Constants

BASE_URL = f"/{Constants.USERS}"


class TestUsersRouter:
    """Test the user router"""

    def test_create_user(self, user_test_service):
        """
        Test create user with email, phone number and both
        """
        user_test_service.create_user_with_email_only()

        user_test_service.create_user_with_phone_number_only()

        user_test_service.create_user_with_phone_number_and_email()

    def test_verify_verification_code(self, user_test_service):
        """
        Test verify verification code with email and phone number
        """

        user_test_service.request_verify_verification_code_email()
        user_test_service.request_verify_verification_code_phone_number()

    def test_send_verification_code(self, user_test_service):
        """
        Test send verification code with email and phone number
        """
        user_test_service.sent_verification_code_for_email()
        user_test_service.sent_verification_code_for_phone_number()

    def test_change_password(self, user_test_service):
        """Test change password with old password and new password"""

        user_test_service.change_password()

    def test_reset_password(self, user_test_service):
        """Test reset password with email and phone number"""
        user_test_service.reset_password()

    def test_submit_reset_password(self, user_test_service):
        """Test submit reset password with email and phone number"""
        user_test_service.submit_reset_password_with_email()
        # user_test_service.submit_reset_password_with_phone_number()

    def test_edit_user(self, user_test_service):
        """Test edit user with first name, last name, address, email, phone number and email redirect url"""
        user_test_service.edit_user()

    def test_get_all_users(self, user_test_service):
        """Test get all users"""
        user_test_service.get_all_users()

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
