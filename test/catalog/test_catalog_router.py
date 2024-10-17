from src.users.users_model import UserRole


class TestCatalogRouter:
    """Test catalog router"""

    def test_catalog_create(self, catalog_test_service):
        """Test create article
        When the user is an admin or a secretary, he can create an article
        But a customer can't create an article
        """
        # Créer un utilisateur secretaire
        catalog_test_service.create_article_with_secretary()

        # créer un utilisateur admin
        catalog_test_service.create_article_with_admin()

        # échouer à un article avec un utilisateur customer
        catalog_test_service.fail_to_create_with_customer()

    def test_catalog_edit(self, catalog_test_service):
        """Test edit article
        When the user is an admin or a secretary, he can edit an article
        But a customer can't edit an article
        """
        # Créer un utilisateur secretaire
        catalog_test_service.edit_article(role=UserRole.SECRETARY)

        # créer un utilisateur admin
        catalog_test_service.edit_article(role=UserRole.ADMIN)

        # échouer à un article avec un utilisateur customer
        catalog_test_service.fail_to_edit_article_with_customer()

    def test_catalog_get_all(self, catalog_test_service):
        """Test get all articles"""
        catalog_test_service.get_all_articles()

    def test_catalog_get_by_id(self, catalog_test_service):
        """Test get article by id"""
        catalog_test_service.get_article_by_id()

    def test_catalog_delete(self, catalog_test_service):
        """Test delete article"""
        catalog_test_service.delete_article_by_id(role=UserRole.ADMIN)
        catalog_test_service.delete_article_by_id(role=UserRole.SECRETARY)
        catalog_test_service.delete_article_customer_by_id()

    def test_catalog_search(self, catalog_test_service):
        """Test search article by name or code"""
        catalog_test_service.search_article_by_name_or_code()
