from test.base_test_service import BaseTestService
from src.utils.constants import Constants
from src.users.users_model import UserRole
from src.utils.error_messages import ErrorMessages

class InvoiceTestService(BaseTestService):
    base_url = f"/{Constants.INVOICES}"

    def __init__(self, get_access_token, get_all_invoices):
        self.get_access_token = get_access_token
        self.invoices = get_all_invoices

    def create_invoice(self, role):
        """Test la création d'une facture."""
        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(self.secretaries[0]["email"], self.password_all_users)
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(self.admins[0]["email"], self.password_all_users)

        invoice_data = self.invoices[0]
        response = self.client.post(
            self.base_url,
            json=invoice_data,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200, "Invoice creation failed"
        assert response.json()["id"] is not None, "Invoice ID should not be None"

    def get_invoice_by_id(self, role):
        """Test la récupération d'une facture."""
        if role == UserRole.SECRETARY:
            access_token = self.get_access_token(self.secretaries[0]["email"], self.password_all_users)
        elif role == UserRole.ADMIN:
            access_token = self.get_access_token(self.admins[0]["email"], self.password_all_users)

        invoice_id = self.invoices[0]["id"]
        response = self.client.get(
            f"{self.base_url}/{invoice_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200, "Failed to get invoice by ID"
        assert response.json()["id"] == invoice_id, "Invoice ID mismatch"
