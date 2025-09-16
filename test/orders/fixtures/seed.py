import pytest
from src.database import SessionLocal

from src.order.order_model import OrderModel


orders = []


@pytest.fixture(scope="session")
def get_all_orders():
    """Retrieve all orders from the database with their IDs."""
    return orders
