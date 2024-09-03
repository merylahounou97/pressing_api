import datetime
from faker import Faker
import random
from src.order.order_enums import OrderTypeEnum
fake = Faker()




def generate_order():
    date = fake.date()
    return {
        "date": date,
        "collect": fake.boolean(),
        "delivery": fake.boolean(),
        "type_order": list([OrderTypeEnum.Express,OrderTypeEnum.Normal])[fake.random_int(min=0,max=1)],
        "delivery_date": fake.date_between(date),
        "order_items": [
            {
                "code": 1,
                "product_id": 1,
                "quantity": 1,
                "unit_price": 100.0,
                "total_price": 100.0,
            }
        ],
    }