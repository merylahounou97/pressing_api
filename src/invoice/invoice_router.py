from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, FileResponse
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

@router.post("/{order_id}", response_class=FileResponse)
def generate_invoice(
    order_id: int,
    invoice_service: InvoiceService = Depends(InvoiceService),
# user=Depends(get_user_online_dep(roles=[UserRole.ADMIN, UserRole.SECRETARY])),
):
    return invoice_service.create_invoice(order_id)

@router.post("/send/{order_id}")
def send_invoice_by_email(
    order_id: int,
    invoice_service: InvoiceService = Depends(InvoiceService),
    # user=Depends(get_user_online_dep(roles=[UserRole.ADMIN, UserRole.SECRETARY])),
):
    """
    Envoie une facture par email. Accessible uniquement aux administrateurs et secrétaires.
    """
    return invoice_service.send_invoice_by_email(order_id)