from src.users.users_model import UserRole


class TestOrderRouter:
    """Test order router"""

    def test_order_create(self, order_test_service):
        """Test create order
        When the user is a customer, he can create an order
        But an admin or a secretary can create an order
        """
        # Créer un utilisateur customer
        order_test_service.create_order(UserRole.CUSTOMER)

        # créer un utilisateur secretaire
        order_test_service.create_order(UserRole.SECRETARY)

        # créer un utilisateur admin
        order_test_service.create_order(UserRole.ADMIN)

        # créer un utilisateur admin
        order_test_service.create_order(UserRole.ADMIN, test_customer_id_asbsence=True)

    def test_order_get_by_id(self, order_test_service):
        """Test get order by id"""
        order_test_service.get_order_by_id(UserRole.SECRETARY)

        order_test_service.get_order_by_id(UserRole.ADMIN)

    def test_order_edit(self, order_test_service):
        """Test edit order
        When the user is a customer, he can't edit an order
        But an admin or a secretary can edit an order
        """
        # Créer un utilisateur customer
        order_test_service.fail_to_edit_order_with_customer()

        # créer un utilisateur secretaire
        order_test_service.edit_order(UserRole.SECRETARY)

        # créer un utilisateur admin
        order_test_service.edit_order(UserRole.ADMIN)

    def test_order_get_all(self, order_test_service):
        """Test get all orders"""
        order_test_service.get_all_orders(UserRole.SECRETARY)
        order_test_service.get_all_orders(UserRole.ADMIN)

        order_test_service.fail_to_get_all_orders_with_customer()


    def test_order_cancel(self, order_test_service):
        """Test cancel order"""
        order_test_service.cancel_order(UserRole.SECRETARY)
        order_test_service.cancel_order(UserRole.ADMIN)
        order_test_service.cancel_order(UserRole.CUSTOMER)

    def test_order_history(self, order_test_service):
        """Test get order history"""
        order_test_service.get_order_history(UserRole.SECRETARY)
        order_test_service.get_order_history(UserRole.ADMIN)
        order_test_service.get_order_history(UserRole.CUSTOMER)
