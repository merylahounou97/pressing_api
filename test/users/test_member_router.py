"""
Créer une classe de *service pour les membres (exemple user_test_service)
Enlever toutes créations de user dans les tests
Et remplacer par les users crées à l'intilisation des tests
"""

from src.users.users_service import UserService
from test.test_init import client

from src.users.users_model import UserRole
from src.utils.constants import Constants
from src.users.users_schemas import UserCreateMemberInput


class TestSecretaryRouter:

    """ "Test all the path in user related to the secretary actions"""

    def test_create_member(self, member_test_service):
        """Test the creation of a secretary"""
        member_test_service.create_member()
