import random
from faker import Faker
from src.catalog.catalog_enums import ArticleSpecificityEnum

faker = Faker()

class GenerateOrderDetails:
    @staticmethod
    def generate_order_details(order_id: int, article_id: int = None):
        """Generate order details"""
        return {
                "order_id": order_id,
                "article_id": article_id,
                "specificity": faker.random_element(elements=ArticleSpecificityEnum), 
                "divider_coef": random.uniform(0.0, 1),
                "multiplier_coef": random.uniform(0.0, 1),
                "discount_article": random.uniform(0.0, 1),
                "quantity": random.randint(1, 100),
            }
        