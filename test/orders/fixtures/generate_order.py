from datetime import datetime
import random
import pytest
from faker import Faker
from src.order.order_enums import OrderStatusEnum, OrderTypeEnum

fake = Faker()

@pytest.fixture(scope="session")
def generate_order(generate_order_details):
    def __generate_order(article_ids: list[str], customer_id: str = None  ):
        date = fake.future_date().isoformat()
        collect_date = fake.future_date(datetime.strptime(date, '%Y-%m-%d')).isoformat()
        return {
            "order_date": date,
            "type_order": fake.enum(OrderTypeEnum).value,
            "delivery_date": fake.future_date(datetime.strptime(collect_date, '%Y-%m-%d')).isoformat(),
            "collect_date": collect_date,
            "collect": fake.boolean(),
            "delivery": fake.boolean(),
            "discount_order": random.uniform(0.0, 1),
            "customer_id": customer_id,
            "status": fake.enum(OrderStatusEnum).value,
            "order_details": [generate_order_details(article_id=id) for id in article_ids]
        }

    return __generate_order
