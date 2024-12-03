import copy
import random
import pytest
from src.catalog.catalog_model import ArticleModel
from src.order.order_model import OrderDetailsModel, OrderModel
from src.users.users_model import UserModel, UserRole
from src.database import Base, engine, SessionLocal
from test.users.fixtures.seed import customers, secretaries, admins
from test.catalog.fixtures import articles
from test.orders.fixtures.seed import orders, get_all_orders


def clean_order(order):
    del order["order_details"]
    return order


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown(generate_user_data, generate_article, generate_order):
    """Fixture pour configurer et détruire la base de données"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # Insérer des utilisateurs dans la base de donnéee
    _customers = [generate_user_data(role=UserRole.CUSTOMER) for _ in range(2)] + [
        generate_user_data(
            role=UserRole.CUSTOMER, email_verified=True, phone_number_verified=True
        )
    ]
    _secretaries = [generate_user_data(role=UserRole.SECRETARY) for _ in range(2)]
    _admins = [
        generate_user_data(role=UserRole.ADMIN, phone_number="+33666495244"),
        generate_user_data(role=UserRole.ADMIN, email="aiounouu@gmail.com"),
    ]

    users = _customers + _secretaries + _admins
    # Insérer des articles dans la base de donnée
    _articles = [generate_article() for _ in range(10)]
    # Insrer des commandes dans la base de donnée
    customers_ids = [customer["id"] for customer in _customers]
    _orders = [
        generate_order(
            article_ids=[article["id"]], customer_id=random.sample(customers_ids, 1)[0]
        )
        for article in _articles[:5]
    ]

    _orders_details = []
    for index, order in enumerate(_orders):
        order_detail = order["order_details"][
            0
        ]  # Because we have only one detail in each order
        _orders_details.extend([{**order_detail, "order_id": index + 1}])

    _orders_db_cleaned = copy.deepcopy(_orders)
    _orders_db = list(map(clean_order, _orders_db_cleaned))

    with SessionLocal() as db:
        db.add_all(map(lambda user: UserModel(**user), users))
        db.commit()

        db.add_all(map(lambda article: ArticleModel(**article), _articles))

        db.add_all(map(lambda order: OrderModel(**order), _orders_db))
        db.commit()

        db.add_all(
            map(lambda order_detail: OrderDetailsModel(**order_detail), _orders_details)
        )

        db.commit()

    customers.extend(_customers)  # type: ignore
    secretaries.extend(_secretaries)  # type: ignore
    admins.extend(_admins)  # type: ignore

    articles.extend(_articles)  # type: ignore
    orders.extend(_orders)  # type: ignore
