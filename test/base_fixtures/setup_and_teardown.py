import copy
import random
import pytest
from src.catalog.catalog_model import ArticleModel
from src.invoice.invoice_model import InvoiceModel
from src.order.order_model import OrderDetailsModel, OrderModel
from src.users.users_model import UserModel, UserRole
from src.database import Base, engine, SessionLocal
from test.users.fixtures.seed import customers, secretaries, admins
from test.catalog.fixtures import articles
from test.orders.fixtures.seed import orders
from src.config import get_settings
from test.invoice.fixtures.seed import invoices

def clean_order(order):
    """Nettoie une commande en supprimant ses détails."""
    del order["order_details"]
    return order


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown(generate_user_data, generate_article, generate_order, generate_invoice):
    """
    Fixture pour configurer et nettoyer la base de données avant et après les tests.
    """
    # Supprime et recrée toutes les tables dans la base de données
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    settings = get_settings()

    # 1. Générer les utilisateurs
    _customers = [generate_user_data(role=UserRole.CUSTOMER) for _ in range(2)] + [
        generate_user_data(
            role=UserRole.CUSTOMER, email_verified=True, phone_number_verified=True
        )
    ]
    _secretaries = [generate_user_data(role=UserRole.SECRETARY) for _ in range(2)]
    _admins = [
        generate_user_data(role=UserRole.ADMIN, phone_number=settings.default_secretary_phone_number),
        generate_user_data(role=UserRole.ADMIN, email= settings.default_admin_email),
    ]

    users = _customers + _secretaries + _admins

    # 2. Générer les articles
    _articles = [generate_article() for _ in range(10)]

    # 3. Générer les commandes
    customers_ids = [customer["id"] for customer in _customers]
    _orders = [
        generate_order(
            article_ids=[article["id"]], customer_id=random.choice(customers_ids)
        )
        for article in _articles[:5]
    ]

    # 4. Générer les détails des commandes
    _orders_details = []
    for index, order in enumerate(_orders):
        order_detail = order["order_details"][0]
        _orders_details.extend([{**order_detail, "order_id": index + 1}])

    _orders_db_cleaned = copy.deepcopy(_orders)
    _orders_db = list(map(clean_order, _orders_db_cleaned))



    # 6. Insérer les données dans la base de données
    with SessionLocal() as db:
        # Insérer les utilisateurs
        db.add_all(map(lambda user: UserModel(**user), users))
        db.commit()

        # Insérer les articles
        db.add_all(map(lambda article: ArticleModel(**article), _articles))
        db.commit()

        # Insérer les commandes
        db.add_all(map(lambda order: OrderModel(**order), _orders_db))
        db.commit()

        # Insérer les détails des commandes
        db.add_all(
            map(lambda order_detail: OrderDetailsModel(**order_detail), _orders_details)
        )
        db.commit()

        # Insérer les factures
            # 5. Générer les factures
        _invoices = [generate_invoice(x) for x in range(len(_orders))]
        db.add_all(map(lambda invoice: InvoiceModel(**dict(invoice)), _invoices))
        db.commit()

    # Étendre les listes pour les rendre disponibles dans les tests
    customers.extend(_customers)  # type: ignore
    secretaries.extend(_secretaries)  # type: ignore
    admins.extend(_admins)  # type: ignore

    articles.extend(_articles)  # type: ignore
    orders.extend(_orders)  # type: ignore
    invoices.extend(_invoices)  # type: ignore
