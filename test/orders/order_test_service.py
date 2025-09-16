# This file contains the test service for the order endpoints.
"""Gerer la suppression des order_details lors de la modification d'une commande
    Envoyer une erreur de token expire lorsque le token est expire plutot qu'une erreur 500
    Finir les tests pour les commandes
"""


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
        get_all_orders,
        generate_order_details,
    ):
        self.get_access_token = get_access_token
        self.generate_order = generate_order
        self.customers = get_all_users
        self.secretaries = get_all_secretaries
        self.admins = get_all_admins
        self.get_number_orders_db = get_number_orders_db
        self.get_all_articles = get_all_articles
        self.orders = get_all_orders
        self.generate_order_details = generate_order_details

    def create_order(self, role, test_customer_id_asbsence=False):
        articles_ids = [article["id"] for article in self.get_all_articles[2:4]]

        order_data = self.generate_order(article_ids=articles_ids)

        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(
                self.secretaries[0]["email"], self.password_all_users
            )
            if not test_customer_id_asbsence:
                order_data["customer_id"] = self.customers[0]["id"]
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(
                self.admins[0]["email"], self.password_all_users
            )
            if not test_customer_id_asbsence:
                order_data["customer_id"] = self.customers[0]["id"]
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
            assert (
                response.status_code == 400
            ), "Failed to create order without customer id"
            assert (
                response.json()["detail"] == ErrorMessages.USER_ID_NOT_PROVIDED
            ), "Customer id should be provided"
        else:
            assert (
                response.status_code == 200
            ), "Failed to create order as admin or secretary"
            response_payload = response.json()
            assert response_payload["id"] is not None, "Order id should not be None"
            assert (
                response_payload["status"] == OrderStatusEnum.PENDING.value
            ), "Order status should be pending"

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

        order_id = 5

        response = self.client.get(
            f"{self.base_url}/{order_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        response_payload = response.json()
        assert response.status_code == 200, "Failed to get order by id"
        assert response_payload["id"] == order_id, "Order id should not change"

    def fail_to_edit_order_with_customer(self):
        """Fail to edit an order with a customer."""
        access_token = self.get_access_token(
            self.customers[0]["email"], self.password_all_users
        )
        edit_data = {"delivery": True, "collect": False}

        order_id = 1
        response = self.client.patch(
            f"{self.base_url}/{order_id}",
            json=edit_data,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 401, "Customer should not be able to edit order"
        assert (
            response.json()["detail"] == ErrorMessages.ACTION_NOT_ALLOWED
        ), "Customer should not be able to edit order"

    def edit_order(
        self,
        role,
    ):
        """Edit an order."""
        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(
                self.secretaries[0]["email"], self.password_all_users
            )
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(
                self.admins[0]["email"], self.password_all_users
            )
        edit_data = self.orders[0]
        edit_data["delivery"] = not edit_data["delivery"]
        edit_data["collect"] = not edit_data["collect"]
        article_id = edit_data["order_details"][0]["article_id"]
        edit_data["order_details"] = [{**edit_data["order_details"][0], "quantity": 20}]

        edit_data["order_details"].append(
            self.generate_order_details(article_id=self.get_all_articles[3]["id"])
        )
        edit_data["articles_to_delete"] = [edit_data["order_details"][1]["article_id"]]

        order_id = 7
        response = self.client.patch(
            f"{self.base_url}/{order_id}",
            json=edit_data,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        response_payload = response.json()
        assert response.status_code == 200, "Order edition failed"
        assert response_payload["id"] == order_id, "Order id should not change"
        assert (
            response_payload["delivery"] == edit_data["delivery"]
        ), "Delivery should change"
        assert (
            response_payload["collect"] == edit_data["collect"]
        ), "Collect should change"

        article_ids = [
            order_detail["article_id"]
            for order_detail in response_payload["order_details"]
        ]
        assert (
            edit_data["order_details"][1]["article_id"] not in article_ids
        ), "Article should be deleted"
        assert (
            edit_data["order_details"][0]["article_id"] in article_ids
        ), "Article should be updated"

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

        assert response.status_code == 200, "Failed to get all orders"

    def fail_to_get_all_orders_with_customer(self):
        """Fail to get all orders with a customer."""
        access_token = self.get_access_token(
            self.customers[0]["email"], self.password_all_users
        )

        response = self.client.get(
            self.base_url,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert (
            response.status_code == 401
        ), "Customer should not be able to get all orders"
        assert (
            response.json()["detail"] == ErrorMessages.ACTION_NOT_ALLOWED
        ), "Customer should not be able to get all orders"

    def cancel_order(self, role):
        """Cancel an order."""
        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(
                self.secretaries[0]["email"], self.password_all_users
            )
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(
                self.admins[0]["email"], self.password_all_users
            )
        else:
            access_token = self.get_access_token(
                self.customers[0]["email"], self.password_all_users
            )

        order_id = 2
        edit_status = {"status": OrderStatusEnum.CANCELED.value}
        response = self.client.patch(
            f"{self.base_url}/cancel/{order_id}",
            json=edit_status,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        response_payload = response.json()
        if role == UserRole.CUSTOMER:
            assert (
                response.status_code == 401
            ), "Customer should not be able to cancel order"
            assert (
                response_payload["detail"] == ErrorMessages.ACTION_NOT_ALLOWED
            ), "Customer should not be able to cancel order"
        else:
            assert response.status_code == 200, "Order cancelation failed"
            assert response_payload["id"] == order_id, "Order id should not change"
            assert (
                response_payload["status"] == OrderStatusEnum.CANCELED.value
            ), "Order status should change"

    def get_order_history(self, role):
        """Get order history."""
        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(
                self.secretaries[0]["email"], self.password_all_users
            )
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(
                self.admins[0]["email"], self.password_all_users
            )
        else:
            access_token = self.get_access_token(
                self.customers[0]["email"], self.password_all_users
            )

        customer_id = self.customers[0]["id"]
        response = self.client.get(
            f"{self.base_url}/history/{customer_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        response_payload = response.json()
        assert response.status_code == 200, "Failed to get order history"
