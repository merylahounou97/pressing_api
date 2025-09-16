from src.users.users_model import UserRole

class TestInvoiceRouter:
    """Test du routeur pour les factures."""

    def test_invoice_create(self, invoice_test_service):
        """Test la création de facture par différents rôles."""
        invoice_test_service.create_invoice(UserRole.SECRETARY)
        invoice_test_service.create_invoice(UserRole.ADMIN)

    def test_invoice_get_by_id(self, invoice_test_service):
        """Test la récupération d'une facture."""
        invoice_test_service.get_invoice_by_id(UserRole.SECRETARY)
        invoice_test_service.get_invoice_by_id(UserRole.ADMIN)
