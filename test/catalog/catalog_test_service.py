from src.users.users_model import UserRole
from test.base_test_service import BaseTestService
from src.utils.constants import Constants
from src.utils.error_messages import ErrorMessages


class CatalogTestService(BaseTestService):
    """This class is used to test the catalog router
    Args:
        generate_user_data (function): A function that generates user data
        create_user (function): A function that creates a user
        get_access_token (function): A function that gets the access token of a user
        generate_article (function): A function that generates article data
    """

    base_url = f"/{Constants.ARTICLES}"

    def __init__(
        self,
        get_access_token,
        generate_article,
        get_all_secretaries,
        get_all_admins,
        get_all_users,
        get_all_articles,
    ):
        self.generate_article = generate_article
        self.get_access_token = get_access_token
        self.secretaries = get_all_secretaries
        self.admins = get_all_admins
        self.customers = get_all_users
        self.articles = get_all_articles

    def check_article_creation(self, response):
        """Check if the article creation was successful
        Args:
            response (response): The response from the article creation
        """
        assert response.status_code == 200, "Article creation failed"
        return response

    def __create_article(self, user):
        """Create an article
        Args:
            user (dict): The user data  to create the article
        """
        access_token = self.get_access_token(user["email"], self.password_all_users)
        # Generate data for article
        item_to_add = self.generate_article()

        response = self.client.post(
            f"{self.base_url}",
            json=item_to_add,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        return response

    def create_article_with_secretary(self):
        """Create an article with a secretary"""
        response = self.__create_article(self.secretaries[0])
        return self.check_article_creation(response)

    def create_article_with_admin(self):
        """Create an article with an admin"""
        response = self.__create_article(self.admins[0])
        return self.check_article_creation(response)

    def fail_to_create_with_customer(self):
        """Fail to create an article with a customer"""
        response = self.__create_article(self.customers[0])
        assert (
            response.status_code == 401
        ), "Customer should not be able to create an article"
        assert (
            response.json()["detail"] == ErrorMessages.ACTION_NOT_ALLOWED
        ), "Customer should not be able to create an article"

    def edit_article(self, role):
        """Edit an article with a secretary or admin"""
        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(
                self.secretaries[0]["email"], self.password_all_users
            )
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(
                self.admins[0]["email"], self.password_all_users
            )

        id_item_to_edit = self.articles[0]["id"]
        data_to_edit = self.generate_article()
        response = self.client.patch(
            f"{self.base_url}/{ id_item_to_edit}",
            json=data_to_edit,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        response_payload = response.json()

        assert response.status_code == 200, "Article edition failed"

        assert response_payload["id"] == id_item_to_edit, "Article id should not change"
        assert (
            response_payload["name"] == data_to_edit["name"]
        ), "Article name should change"
        assert (
            response_payload["description"] == data_to_edit["description"]
        ), "Article description should change"
        assert (
            response_payload["price"] == data_to_edit["price"]
        ), "Article price should change"
        assert (
            response_payload["express_price"] == data_to_edit["express_price"]
        ), "Article express price should change"
        assert (
            response_payload["code"] == data_to_edit["code"]
        ), "Article code should change"

    def fail_to_edit_article_with_customer(self):
        """Fail to edit an article with a customer"""
        access_token = self.get_access_token(
            self.customers[0]["email"], self.password_all_users
        )
        id_item_to_edit = self.articles[0]["id"]
        data_to_edit = self.generate_article()
        response = self.client.patch(
            f"{self.base_url}/{id_item_to_edit}",
            json=data_to_edit,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert (
            response.status_code == 401
        ), "Customer should not be able to edit an article"
        assert (
            response.json()["detail"] == ErrorMessages.ACTION_NOT_ALLOWED
        ), "Customer should not be able to edit an article"
