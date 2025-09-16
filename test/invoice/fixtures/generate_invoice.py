import random
from datetime import datetime, timedelta
from uuid import uuid4
import pytest
from src.invoice.invoice_model import InvoiceModel, InvoiceItemModel

@pytest.fixture(scope="session")
def generate_invoice():
    """Retourne une fonction pour générer des données de factures."""
    def _generate_invoice():
        items = [
            InvoiceItemModel(
                article_name=f"Article {random.randint(1, 10)}",
                specificity="NONE",
                quantity=random.randint(1, 5),
                unit_price=random.uniform(10.0, 100.0),
                total_price=random.uniform(50.0, 500.0),
                discount=random.uniform(0.0, 10.0),
            )
            for _ in range(random.randint(1, 3))
        ]
        return {
            "invoice_date": datetime.utcnow(),
            "due_date": datetime.utcnow() + timedelta(days=7),
            "customer_name": f"Customer {random.randint(1, 1000)}",
            "customer_reference": str(uuid4()),
            "order_id": random.randint(1, 100),
            "total_amount": sum(item.total_price for item in items),
            "discounted_amount": sum(item.total_price - item.discount for item in items),
            "net_amount": sum(item.total_price - item.discount for item in items),
            "items": items,
        }

    return _generate_invoice
