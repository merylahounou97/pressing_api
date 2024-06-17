from src.sms.templates import messages
from twilio.rest import Client

from src.config import Settings
from src.customer.customer_model import CustomerModel


settings = Settings()

TWILIO_ACCOUNT_SID = settings.twilio_account_sid
TWILIO_AUTH_TOKEN = settings.twilio_auth_token
TWILIO_PHONE_NUMBER = settings.twilio_phone_number
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_verification_sms(phone_number: str, verification_code: str):
    """Send verification SMS

    Args:
        phone_number (str): Phone number
        verification_code (str): Verification code
    """
    return __send_sms(
        phone_number, f"Votre code de vérification est {verification_code}"
    )


def send_welcome_sms(customer: CustomerModel):
    """Send welcome SMS

    Args:
        phone_number (str): Phone number
    """
    return __send_sms(
        customer.phone_number,
        f"""Bienvenue chez {settings.app_name}
                      Le code de vérification de votre numéro de téléphone est {customer.phone_number_verification_code}
                      """,
    )


def send_sms(phone_number: str, template_name: str, **kwargs):
    """Send SMS

    Args:
        phone_number (str): Phone number
        message (str): Message
    """
    # Envoyer le SMS de vérificatio
    sms_template = __get_sms_template(template_name, **kwargs)
    __send_sms(phone_number, sms_template)


def __get_sms_template(template_name: str, **kwargs):
    """Get SMS template

    Args:
        template_name (str): Template name

    Returns:
        str: SMS template
    """
    sms_template = messages.sms_messages[template_name](**kwargs)
    return sms_template


def __send_sms(phone_number: str, message: str):
    """Send SMS

    Args:
        phone_number (str): Phone number
        message (str): Message
    """
    # Envoyer le SMS de vérification
    twilio_client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number,
    ) if settings.test_mode is False else None
