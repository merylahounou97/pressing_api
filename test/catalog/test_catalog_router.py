"""
Ecrie un test pour recupérer tous les articles
Ecrire un test pour rcupérer un article  par son id
Ecrire un test pour supprimer un article par son id
Ecrire un test pour rechercher un article par son nom ou son code
"""

from src.users.users_model import UserRole

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

    def test_catalog_edit(self,catalog_test_service):
        """Test edit article
        When the user is an admin or a secretary, he can edit an article
        But a customer can't edit an article
        """
        #Créer un utilisateur secretaire 
        catalog_test_service.edit_article(role=UserRole.SECRETARY)

        # créer un utilisateur admin
        catalog_test_service.edit_article(role=UserRole.ADMIN)

        #échouer à un article avec un utilisateur customer
        catalog_test_service.fail_to_edit_article_with_customer()
        