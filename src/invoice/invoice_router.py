from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from .invoice_service import InvoiceService
from src.users.users_router import get_user_online_dep
from src.users.users_model import UserRole
from src.utils.constants import Constants
from .invoice_schema import InvoiceSchema  # Importer le schéma

router = APIRouter(prefix=f"/{Constants.INVOICES}", tags=[Constants.INVOICES])

@router.post("/generate-invoice", response_class=HTMLResponse)
async def generate_invoice(
    invoice_data: InvoiceSchema,  # Utilisation du schéma Pydantic
    invoice_service: InvoiceService = Depends(InvoiceService),
    user=Depends(get_user_online_dep(roles=[UserRole.ADMIN, UserRole.SECRETARY])),
):
    """
    Génère une facture HTML. Accessible uniquement aux administrateurs et secrétaires.
    """
    # Conversion du schéma en dictionnaire pour le service
    return invoice_service.generate_invoice_html(invoice_data.dict())
