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

    def get_all_articles(self):
        """Test pour récupérer tous les articles"""
        response = self.client.get(f"/{Constants.ARTICLES}")

        # Vérification du succès de la requête
        assert response.status_code == 200, "Échec de la récupération des articles"

        # Vérifier que la réponse contient des articles
        articles = response.json()
        assert isinstance(articles, list), "La réponse doit être une liste d'articles"
        assert len(articles) > 0, "La liste des articles ne doit pas être vide"

    def get_article_by_id(self):
        """Test pour récupérer un article par son ID"""
        article_id = self.articles[0]["id"]  # Prendre l'ID du premier article
        response = self.client.get(f"/{Constants.ARTICLES}/{article_id}")

        # Vérification du succès de la requête
        assert response.status_code == 200, "Échec de la récupération de l'article"

        # Vérifier que l'article retourné correspond à l'ID demandé
        article = response.json()
        assert article["id"] == article_id, "L'ID de l'article ne correspond pas"

    def delete_article_customer_by_id(self):
        """Test pour supprimer un article par son ID"""
        access_token = self.get_access_token(
            self.customers[0]["email"], self.password_all_users
        )
        # Prendre un article
        article_id = self.articles[0]["id"]

        response = self.client.delete(
            f"/{Constants.ARTICLES}/{article_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )   

        # Vérification de l'échec de la suppression
        assert response.status_code == 401, "La suppression de l'article devrait échouer"
        
        assert response.json()["detail"] == ErrorMessages.ACTION_NOT_ALLOWED, "La suppression de l'article devrait échouer"


    def delete_article_by_id(self,role : UserRole):
        """Test pour supprimer un article par son ID"""
        if  role==UserRole. ADMIN:
            access_token = self.get_access_token(
                self.admins[0]["email"], self.password_all_users
            )
            # Prendre un article
            article_id = self.articles[0]["id"]  # Prendre l'ID du premier article
        elif role==UserRole.SECRETARY:
            access_token = self.get_access_token(
                self.secretaries[0]["email"], self.password_all_users
            )
            # Prendre un article
            article_id = self.articles[1]["id"]

        response = self.client.delete(
            f"/{Constants.ARTICLES}/{article_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        

        # Vérification du succès de la suppression
        assert response.status_code == 200, "Échec de la suppression de l'article"
        assert response.json() == article_id, "L'article devrait être supprimé"

        # Vérifier que l'article n'existe plus
        get_response = self.client.get(f"/{Constants.ARTICLES}/{article_id}")
        assert get_response.status_code == 200, "L'article devrait être supprimé"
        assert get_response.json() is None, "L'article devrait être supprimé"

    def search_article_by_name_or_code(self):
        """Test pour rechercher un article par son nom ou son code"""
        article = self.articles[2]
        search_name = article["name"]
        search_code = article["code"]

        # Recherche par nom
        response_by_name = self.client.get(
            f"/{Constants.ARTICLES}?search={search_name}"
        )
        assert response_by_name.status_code == 200, "Échec de la recherche par nom"
        articles_by_name = response_by_name.json()

        assert any(
            search_name in a["name"]   for a in articles_by_name
        ), "Aucun article trouvé par le nom"

        # Recherche par code
        response_by_code = self.client.get(
            f"/{Constants.ARTICLES}?search={search_code}"
        )
        assert response_by_code.status_code == 200, "Échec de la recherche par code"
        articles_by_code = response_by_code.json()
        assert any(
           search_code in  a["code"]  for a in articles_by_code
        ), "Aucun article trouvé par le code"
