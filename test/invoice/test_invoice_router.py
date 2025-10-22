from src.users.users_model import UserRole

class TestInvoiceRouter:
    """Test du routeur pour les factures."""

    def test_invoice_create(self, invoice_test_service):
        """Test la création de facture par différents rôles."""
        invoice_test_service.create_invoice(UserRole.SECRETARY)
        invoice_test_service.create_invoice(UserRole.ADMIN)

    def test_invoice_send_by_email(self, invoice_test_service):
        """Test l'envoi de la facture par email."""
        # Implémenter le test pour l'envoi par email si nécessaire
        invoice_test_service.send_invoice_by_email(UserRole.SECRETARY)
        invoice_test_service.send_invoice_by_email(UserRole.ADMIN)