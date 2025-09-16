import pytest
from test.catalog.catalog_test_service import CatalogTestService


@pytest.fixture
def catalog_test_service(
    get_access_token,
    generate_article,
    get_all_secretaries,
    get_all_admins,
    get_all_users,
    get_all_articles,
):
    return CatalogTestService(
        get_access_token,
        generate_article,
        get_all_secretaries,
        get_all_admins,
        get_all_users,
        get_all_articles,
    )
