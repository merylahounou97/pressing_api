import uuid
import pytest
from faker import Faker
import random

from src.catalog.catalog_enums import (
    ArticleCategoryEnum,
    ArticleFreqEnum,
    ArticleStatusEnum,
)


fake = Faker()


@pytest.fixture(scope="session")
def generate_article():
    def _generate_article():
        return {
            "id": str(uuid.uuid4()),
            "name": fake.word(),
            "code": fake.word(),
            "description": fake.text(),
            "details": fake.text(),
            "category": fake.enum(ArticleCategoryEnum).value,
            "status": fake.enum(ArticleStatusEnum).value,
            "freq": fake.enum(ArticleFreqEnum).value,
            "price": random.randint(100, 1000),
            "express_price": random.randint(100, 1000),
        }

    return _generate_article
