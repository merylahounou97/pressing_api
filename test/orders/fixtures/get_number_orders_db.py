import pytest
from src.order.order_model import OrderModel


@pytest.fixture(scope="session")
def get_number_orders_db(get_test_db_session):
    """Get the number of orders in the database"""
    return get_test_db_session.query(OrderModel).count()
