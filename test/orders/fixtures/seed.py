import pytest


orders = []


@pytest.fixture(scope="session")
def get_all_orders():
    """Fixture to get all orders."""
    return orders

