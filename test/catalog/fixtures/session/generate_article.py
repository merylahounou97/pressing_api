import uuid
import pytest
from faker import Faker
import random


fake = Faker()


@pytest.fixture(scope="session")
def generate_article():
    def _generate_article():
        return {
            "id": str(uuid.uuid4()),
            "name": fake.word(),
            "description": fake.text(),
            "price": random.randint(100, 1000),
            "express_price": random.randint(100, 1000),
            "code": fake.word(),
        }

    return _generate_article
