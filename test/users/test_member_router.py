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


BASE_URL = f"{Constants.MEMBER}"

class  TestSecretaryRouter():
    """"Test all the path in user related to the secretary actions"""
    def test_create_member(self,generate_user_data,get_access_token,create_user):
        """Test the creation of a secretary"""

        # #Log with a user that is not an admin
        customer_data= generate_user_data(UserRole.CUSTOMER)
        customer = create_user(customer_data)

        access_token = get_access_token(customer.email,customer_data["password"])
        user = generate_user_data(UserRole.SECRETARY)
        response = client.post(BASE_URL, json=user,headers={"Authorization": f"Bearer {access_token}"})
        
        #Creation should fail
        assert response.status_code == 401, "Error for creating a secretary with a non admin user failed"
        

        #Log in an admin to create a secretary
        admin_data = UserService.get_default_admin_input()
        
        #First create the admin
        admin=create_user(admin_data,is_member=True)
        admin_token = get_access_token(admin.email, admin_data["password"])
        response = client.post(BASE_URL, json=user,headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200, "Secretary creation failed"

        #Test the creation of an admin
        user_data = generate_user_data(UserRole.ADMIN)
        response = client.post(BASE_URL,json=user_data,headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200, "Admin creation failed"
