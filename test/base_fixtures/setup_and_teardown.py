import pytest
from src.catalog.catalog_model import ArticleModel
from src.order.order_model import OrderModel
from src.users.users_model import UserModel, UserRole
from src.database import Base, engine, SessionLocal
from test.users.fixtures.session.seed import *
from test.catalog.fixtures.session.seed import *
from test.orders.fixtures.session.seed import *


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
    _articles = [generate_article() for _ in range(4)]
        #Insrer des commandes dans la base de donnée
    _orders = [generate_order() for _ in range(4)]
    with SessionLocal() as db:
        for user in users:
            db.add(UserModel(**user))
        for article in _articles:
            db.add(ArticleModel(**article))
        for order in _orders:
            # print(order)
            continue
        db.commit()


    customers.extend(_customers)  # type: ignore
    secretaries.extend(_secretaries)  # type: ignore
    admins.extend(_admins)  # type: ignor

    articles.extend(_articles)  # type: ignore
    orders.extend(_orders)  # type: ignore

