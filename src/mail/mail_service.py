from fastapi import  HTTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from  src.config import Settings
from fastapi.templating import Jinja2Templates

from src.person.person_schema import Person

from ..dependencies.get_api_url import get_api_url



settings = Settings()

api_url = get_api_url()

templates = Jinja2Templates(directory="src/mail/templates")



async def  send_welcome_email(person: Person):
    mail_content = get_parsed_template(template_name="welcome.html",person=person,app_name="WashMan",api_url=api_url)
    return  send_email(person.email,f"Bienvenue à WashMan , {person.first_name} ! Prêt à simplifier votre routine de nettoyage ?",mail_content)

def get_parsed_template(template_name: str,**kargs):
    email_template = templates.get_template(template_name)
    return email_template.render(kargs )

def send_email(to: str, subject: str,email_content: str):
    sender_email = settings.sender_email
    sender_password = settings.mail_password

    # Création du message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to
    message["Subject"] = subject
    
    # Ajout du corps du message
    message.attach(MIMEText(email_content, "html"))
    
    try:
        # Connexion au serveur SMTP de Gmail
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Active la sécurité TLS
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to, message.as_string())
            return {"status": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
