import pytest


# Liste globale pour stocker les factures
invoices = []

@pytest.fixture(scope="session")
def get_all_invoices():
    """Renvoie toutes les factures."""
    return invoices

