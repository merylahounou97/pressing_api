from datetime import datetime
import random
import pytest
from faker import Faker
from src.order.order_enums import OrderStatusEnum, OrderTypeEnum

fake = Faker()

@pytest.fixture(scope="session")
def generate_order():
    def __generate_order(customer_id: str = None):
        date = fake.future_date()
        collect_date = fake.future_date(date)
        return {
            "order_date": date, 
            "type_order": list([OrderTypeEnum.Express, OrderTypeEnum.Normal])[
                fake.random_int(min=0, max=1)
            ],
            "delivery_date":  fake.future_date(collect_date) ,
            "collect_date": collect_date ,
            "collect": fake.boolean(),
            "delivery": fake.boolean(),
            "discount_order": random.uniform(0.0, 1),
            "customer_id":customer_id,
            "status": fake.random_element(elements=OrderStatusEnum),
        }
    return __generate_order    
