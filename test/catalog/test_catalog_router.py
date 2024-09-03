from test.catalog.conftest import catalog_test_service


class TestCatalogRouter:
    """Test catalog router
    """
    def test_catalog_create(self,catalog_test_service):
        """Test create article
        When the user is an admin or a secretary, he can create an article
        But a customer can't create an article
        """
        #Créer un utilisateur secretaire 
        catalog_test_service.create_article_with_secretary()

        # créer un utilisateur admin
        catalog_test_service.create_article_with_admin()

        #échouer à un article avec un utilisateur customer
        catalog_test_service.fail_to_create_with_customer()
        