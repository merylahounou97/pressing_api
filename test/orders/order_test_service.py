from src.order.order_enums import OrderStatusEnum
from src.utils.constants import Constants
from src.users.users_model import UserRole
from src.utils.error_messages import ErrorMessages
from test.base_test_service import BaseTestService


class OrderTestService(BaseTestService):
    base_url = f"/{Constants.ORDERS}"

    def __init__(
        self,
        get_access_token,
        generate_order,
        get_all_users,
        get_all_secretaries,
        get_all_admins,
        get_number_orders_db,
        get_all_articles,

    ):
        self.get_access_token = get_access_token
        self.generate_order = generate_order
        self.customers = get_all_users
        self.secretaries = get_all_secretaries
        self.admins = get_all_admins
        self.get_number_orders_db = get_number_orders_db
        self.get_all_articles = get_all_articles

    def create_order(self, role, test_customer_id_asbsence=False):
        articles_ids = [article["id"] for article in self.get_all_articles[2:] ] 

        order_data =  self.generate_order(article_ids=articles_ids)

        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(
                self.secretaries[0]["email"], self.password_all_users
            )
            if not test_customer_id_asbsence:    order_data["customer_id"] = self.customers[0]["id"]
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(
                self.admins[0]["email"], self.password_all_users
            )
            if not test_customer_id_asbsence:    order_data["customer_id"] = self.customers[0]["id"]
        else:
            access_token = self.get_access_token(
                self.customers[0]["email"], self.password_all_users
            )
            
         # Générer des données de commande avec la fonction generate_order

        response = self.client.post(
            self.base_url,
            json=order_data,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if test_customer_id_asbsence:
            assert response.status_code == 400, "Failed to create order without customer id"
            assert response.json()["detail"] == ErrorMessages.USER_ID_NOT_PROVIDED, "Customer id should be provided"
        else:
            assert response.status_code == 200, "Failed to create order as admin or secretary"
            response_payload = response.json()
            assert response_payload["id"] is not None, "Order id should not be None"
            assert response_payload["status"] == OrderStatusEnum.PENDING.value, "Order status should be pending"

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
        order_id = self.get_all_orders()[0]["id"]
        response = self.client.patch(
            f"{self.base_url}/{order_id}",
            json=edit_data,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        response_payload = response.json()
        assert response.status_code == 200, "Order edition failed"
        assert response_payload["id"] == order_id, "Order id should not change"
        assert response_payload["delivery"] == edit_data["delivery"], "Delivery should change"
        assert response_payload["collect"] == edit_data["collect"], "Collect should change"


    def fail_to_edit_order_with_customer(self):
        """Fail to edit an order with a customer."""
        access_token = self.get_access_token(
            self.customers[0]["email"], self.password_all_users
        )
        edit_data = {"delivery": True, "collect": False}
        order_id = self.get_all_orders()[0]["id"]
        response = self.client.patch(
            f"{self.base_url}/{order_id}",
            json=edit_data,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 401, "Customer should not be able to edit order"
        assert response.json()["detail"] == Constants.ACTION_NOT_ALLOWED, "Customer should not be able to edit order"

    def get_all_orders(self, role):
        """Get all orders."""
        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(
                self.secretaries[0]["email"], self.password_all_users
            )
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(
                self.admins[0]["email"], self.password_all_users
            )
        
        response = self.client.get(
            self.base_url,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        response_payload = response.json()
        assert response.status_code == 200, "Failed to get all orders"
        assert len(response_payload) > 0, "There should be at least one order"  # Vérifiez qu'il y a au moins une commande

    def get_order_by_id(self, role):
        """Get order by id."""
        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(
                self.secretaries[0]["email"], self.password_all_users
            )
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(
                self.admins[0]["email"], self.password_all_users
            )

        order_id = self.get_all_orders()[0]["id"]
        response = self.client.get(
            f"{self.base_url}/{order_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        response_payload = response.json()
        assert response.status_code == 200, "Failed to get order by id"
        assert response_payload["id"] == order_id, "Order id should not change"

    def delete_order_by_id(self, role):
        """Delete order by id."""
        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(
                self.secretaries[0]["email"], self.password_all_users
            )
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(
                self.admins[0]["email"], self.password_all_users
            )

        order_id = self.get_all_orders()[0]["id"]
        response = self.client.delete(
            f"{self.base_url}/{order_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200, "Failed to delete order by id"
        assert response.json() == Constants.ORDER_DELETED, "Order should be deleted"

    def delete_order_customer_by_id(self):
        """Delete order by id as customer."""
        access_token = self.get_access_token(
            self.customers[0]["email"], self.password_all_users
        )
        order_id = self.get_all_orders()[0]["id"]
        response = self.client.delete(
            f"{self.base_url}/{order_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 401, "Customer should not be able to delete order"
        assert response.json()["detail"] == Constants.ACTION_NOT_ALLOWED, "Customer should not be able to delete order"

    def search_order_by_name_or_id(self,role):
        """Search order by name or id."""
        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(
                self.secretaries[0]["email"], self.password_all_users
            )
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(
                self.admins[0]["email"], self.password_all_users
            )

        order_id = self.get_all_orders()[0]["id"]
        order_name = self.get_all_orders()[0]["name"]
        response = self.client.get(
            f"{self.base_url}/search?name={order_name}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        response_payload = response.json()
        assert response.status_code == 200, "Failed to search order by name"
        assert response_payload[0]["name"] == order_name, "Order name should not change"

        response = self.client.get(
            f"{self.base_url}/search?id={order_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        response_payload = response.json()
        assert response.status_code == 200, "Failed to search order by id"
        assert response_payload[0]["id"] == order_id, "Order id should not change"
