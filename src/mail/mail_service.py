import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from fastapi import HTTPException
from fastapi.templating import Jinja2Templates

from src.config import Settings

from ..dependencies.get_api_url import get_api_url

settings = Settings()
templates = Jinja2Templates(directory="src/mail/templates")
api_url = get_api_url()


def send_mail_from_template(template_name: str, email: str, **kwargs):
    """Send an email from a template.

    Args:
        template_name (str): The name of the template.
        **kwargs (dict): The template variables.

    Returns:
        dict: The status of the email sending.
    """

    mail_content = __get_parsed_template(template_name=template_name, **kwargs)
    return (
        __send_email(email, "WashMan", mail_content) if settings.ENV != "test" else None
    )


def parse_validation_email(redirect_url: str, verification_code_email: str, email: str):
    """Parse the validation email

    Args:
        redirect_url (str): Redirect URL
        verification_code_email (str): Verification code
        email (str): Email

    Returns:
        str: Redirect URL
    """
    if settings.ENV == "dev":
        redirect_url = get_api_url()
    return f"{redirect_url}?code={verification_code_email}&identifier={email}"


def __get_parsed_template(template_name: str, **kargs):
    """Parse a Jinja2 template with the given arguments.

    Args:
        template_name (str): The name of the template.
        **kargs: The arguments to pass to the template.

    Returns:
        str: The parsed template.
    """
    email_template = templates.get_template(template_name)
    return email_template.render({**kargs, "api_url": api_url})

def send_email(to: str, subject: str, email_content: str, attachment_path=None):
    return __send_email(to, subject, email_content, attachment_path)

def __send_email(to: str, subject: str, email_content: str, attachment_path=None):
    """Send an email to the given recipient.

    Args:
        to (str): The recipient's email address.
        subject (str): The subject of the email.
        email_content (str): The content of the email.

    Returns:
        dict: The status of the email sending.
    """
    sender_email = settings.sender_email
    sender_password = settings.mail_password

    # Création du message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to
    message["Subject"] = subject

    # Ajout du corps du message
    message.attach(MIMEText(email_content, "html"))

    if attachment_path:
        # Ajout de la pièce jointe
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {attachment_path.split('/')[-1]}",
            )
            message.attach(part)



    try:
        # Connexion au serveur SMTP de Gmail
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Active la sécurité TLS
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to, message.as_string())
            return {"status": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

