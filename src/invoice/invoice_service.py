"""
Amélioration de la génération de facture, pour qu'elle soit identique au fichier excel de base.
Dans le parametre envoy  la fonction render qui genere le template, on ajoute les informations du customer.
Les totaux necessaires sur la facture.
Reflechir  de la suppression des articles de la base.
"""



from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.dependencies.db import get_db
from jinja2 import Template
from src.order.order_service import OrderService
from src.users.users_service import UserService
import os
from weasyprint import HTML
from src.mail import mail_service
from datetime import timedelta

from pathlib import Path


from fastapi.templating import Jinja2Templates
from ..dependencies.get_api_url import get_api_url



templates = Jinja2Templates(directory="src/invoice/template")

api_url = get_api_url()

class InvoiceService:
    def __init__(self, db: Session = Depends(get_db)):
        self.template_path = Path(__file__).parent / "template" / "invoice.html"
        self.db = db

    # def generate_invoice_html(self, invoice_data: dict) -> str:
    #     """
    #     Génère le HTML d'une facture à partir des données fournies.
    #     """
    #     try:
    #         # Chargement du template
    #         with open(self.template_path, "r", encoding="utf-8") as file:
    #             template_content = file.read()
    #         template = Template(template_content)
    #         return template.render(invoice_data)
    #     except FileNotFoundError:
    #         raise HTTPException(status_code=500, detail="Le fichier template HTML est introuvable.")
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de la facture : {str(e)}")


    def create_invoice(self, order_id: int):
        """
        Crée une facture à partir d'une commande.
        """
        order_service = OrderService(self.db)

        order = order_service.get_order(order_id)

        # template = templates.get_template("order_invoice.html")
        template = templates.get_template("gemini.html")   
        # template = templates.get_template("gpt.html")               
                                        
        invoice_content = template.render(order=order,api_url=api_url, timedelta=timedelta)

        # 2. Conversion du HTML en PDF avec WeasyPrint
        invoices_dir = "/tmp/invoices"

        pdf_file = f"{invoices_dir}/{order_id}.pdf"

        os.makedirs(invoices_dir, exist_ok=True)

        HTML(string=invoice_content).write_pdf(pdf_file)

        return pdf_file

    def send_invoice_by_email(self, order_id: int):
        """
        Envoie une facture par email.
        """

        order_service = OrderService(self.db)
        users_service = UserService(self.db)

        order = order_service.get_order(order_id)

        user = users_service.get_user_by_id(order.customer_id)

        pdf_file = self.create_invoice(order_id)
        # Envoi de l'email
        return mail_service.send_email(
            to=user.email ,
            subject="Votre facture",
            email_content=f"Bonjour, veuillez trouver en pièce jointe votre facture.",
            attachment_path=pdf_file)