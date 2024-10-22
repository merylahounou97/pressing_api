import uuid
import pytest
from faker import Faker
import random

from src.catalog.catalog_enums import ArticleCategoryEnum, ArticleFreqEnum, ArticleStatusEnum


fake = Faker()


@pytest.fixture(scope="session")
def generate_article():
    def _generate_article():
        return {
            "id": random.randint(1, 1000),
            "name": fake.word(),
            "code": fake.word(),
            "description": fake.text(),
            "details": fake.text(),
            "category": fake.enum(ArticleCategoryEnum) ,
            "status": fake.enum(ArticleStatusEnum),
            "freq": fake.enum(ArticleFreqEnum),
            "price": random.randint(100, 1000),
            "express_price": random.randint(100, 1000),
        }

    return _generate_article
