import random

import pytest
from faker import Faker
from src.catalog.catalog_enums import ArticleSpecificityEnum

faker = Faker()


@pytest.fixture(scope="session")
def generate_order_details():
    def __generate_order_details(article_id: str = None):
        """Generate order details"""
        return {
            "article_id": article_id,
            "specificity": faker.enum(ArticleSpecificityEnum).value,
            "divider_coef": random.uniform(0.0, 1),
            "multiplier_coef": random.uniform(0.0, 1),
            "discount_article": random.uniform(0.0, 1),
            "quantity": random.randint(1, 100),
        }

    return __generate_order_details
