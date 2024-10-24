from src.utils.constants import Constants
from src.users.users_model import UserRole

class OrderTestService:
    base_url = f"/{Constants.ORDERS}"

    def __init__(self, client, get_access_token, generate_order):
        self.client = client
        self.get_access_token = get_access_token
        self.generate_order = generate_order

    def create_order_as_customer(self):
        """Create an order as a customer."""
        access_token = self.get_access_token(self.customer[0]["email"])
        order_data = self.generate_order()  # Générer des données de commande avec la fonction generate_order
        response = self.client.post(
            self.base_url,
            json=order_data,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200, "Failed to create order as customer"


    def create_order(self, role):
        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(
                self.secretaries[0]["email"], self.password_all_users
            )
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(
                self.admins[0]["email"], self.password_all_users
            )


        order_data = generate_order()

        response = self.client.post(
            self.base_url,
            json=order_data,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200, "Failed to create order as admin"
   

    def edit_order(self, role):
        """Edit an order."""
        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(
                self.secretaries[0]["email"], self.password_all_users
            )
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(
                self.admins[0]["email"], self.password_all_users
            )
        edit_data = {"delivery": True, "collect": False}



