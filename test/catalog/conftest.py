import pytest
from faker import Faker
import random

from test.catalog.catalog_test_service import CatalogTestService
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
def catalog_test_service(generate_user_data,create_user,get_access_token,generate_article):
    return CatalogTestService(generate_user_data,create_user,get_access_token,generate_article)