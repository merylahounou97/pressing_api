import pytest
from test.invoice.invoice_test_service import InvoiceTestService

@pytest.fixture
def invoice_test_service(get_access_token, get_all_invoices):
    """Factory pour le service de test des factures."""
    return InvoiceTestService(
        get_access_token=get_access_token,
        get_all_invoices=get_all_invoices,
    )
