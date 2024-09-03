
from src.utils.constants import Constants
from test.base_test_service import BaseTestService
from test.test_init import client
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

    def __init__(self, generate_user_data, create_user, get_access_token, generate_article):
        super().__init__(generate_user_data, create_user, get_access_token)
        self.generate_article = generate_article

   
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
        access_token = self.get_access_token(user["email"], user["password"])
        # Generate data for article
        item_to_add = self.generate_article()

        response = client.post(
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
        assert response. status_code == 401, "Customer should not be able to create an article"
        assert response.json()["detail"] == ErrorMessages.ACTION_NOT_ALLOWED, "Customer should not be able to create an article"
