from test.base_test_service import BaseTestService
from src.utils.constants import Constants
from src.users.users_model import UserRole
from src.invoice.invoice_router import send_invoice_by_email

class InvoiceTestService(BaseTestService):
    base_url = f"/{Constants.INVOICES}"

    def __init__(self, get_access_token, get_all_invoices, get_all_admins,
        get_all_secretaries):
        self.get_access_token = get_access_token
        self.invoices = get_all_invoices
        self.admins = get_all_admins
        self.secretaries = get_all_secretaries

    def create_invoice(self, role):
        """Test la création d'une facture."""
        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(self.secretaries[0]["email"], self.password_all_users)
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(self.admins[0]["email"], self.password_all_users)

        response = self.client.post(
            f"{self.base_url}/2",

            headers={"Authorization": f"Bearer {access_token}"},
        )



        assert response.status_code == 200, "Invoice creation failed"
        assert ".pdf" in  response.text, "Invalid invoice file path returned"

    def send_invoice_by_email(self, role):
        """Test l'envoi d'une facture par email."""
        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(self.secretaries[0]["email"], self.password_all_users)
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(self.admins[0]["email"], self.password_all_users)

        response = self.client.post(
            f"{self.base_url}/send/2",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200, "Sending invoice by email failed"
        assert response.json()["status"] == "Email sent successfully", "Email sending status incorrect"