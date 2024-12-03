import pytest

from test.orders.order_test_service import OrderTestService


@pytest.fixture
def order_test_service(
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
    return OrderTestService(
        get_access_token,
        generate_order,
        get_all_users,
        get_all_secretaries,
        get_all_admins,
        get_number_orders_db,
        get_all_articles,
        get_all_orders,
        generate_order_details,
    )
