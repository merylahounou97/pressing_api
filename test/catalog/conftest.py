import pytest
from faker import Faker
import random

from test.catalog.catalog_test_service import CatalogTestService
from src.users.users_router import get_all_users
fake = Faker()



@pytest.fixture
def generate_article():
    def _generate_article():
        return {
            "name": fake.word(),
            "description": fake.text(),
            "price": random.randint(100, 1000),
            "express_price": random.randint(100, 1000),
            "code": fake.word(),
        }
    return _generate_article


@pytest.fixture
def catalog_test_service(get_access_token,generate_article,get_all_secretaries,get_all_admins,get_all_users):
    return CatalogTestService(get_access_token,generate_article,get_all_secretaries,get_all_admins,get_all_users)