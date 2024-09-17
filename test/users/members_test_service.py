from src.users.users_model import UserRole
from src.utils.constants import Constants
from test.users.users_test_service import UserTestService


class MembersTestService(UserTestService):
    base_url =  f"/{Constants.MEMBER}"

    def create_member(self):
        """Create a member"""
        # #Log with a user that is not an admin
        customer= self.all_users[0]
        access_token =self. get_access_token(customer["email"],self.password)
        user = self.generate_user_data(role =UserRole.SECRETARY)
        response = self.client.post(self.base_url, json=user,headers={"Authorization": f"Bearer {access_token}"})
        
        #Creation should fail
        assert response.status_code == 401, "Error for creating a secretary with a non admin user failed"
        

        # #Log in an admin to create a secretary
        admin=self.admins[0]
        admin_token = self.get_access_token(admin["email"], self.password)
        response = self.client.post(self.base_url, json=user,headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200, "Secretary creation failed"

        #Test the creation of an admin
        user_data = self.generate_user_data(UserRole.ADMIN)
        response = self. client.post(self.base_url,json=user_data,headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200, "Admin creation failed"