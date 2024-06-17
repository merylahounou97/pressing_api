from src.customer.customer_model import CustomerModel
from src.utils.sms_constants import SmsConstants


def password_changed(customer: CustomerModel, support_address: str):
    """return email template when a password is changed

    Args:
        customer (Customer_model): Customer object
        support_address (str): Support address

        Returns:
            str: The email content
    """
    return f"""
    Bonjour {customer.first_name},
    Votre mot de passe a bien été modifié.
    Merci de vous reconnecter avec votre nouveau mot de passe.
    Si vous n'êtes pas à l'origine de cette demande, veuillez
    nous contacter à l'adresse {support_address}.
"""


def password_reset(customer: CustomerModel):
    """return email template when a password is reset

    Args:
        customer (Customer_model): Customer object
        support_address (str): Support address

        Returns:
            str: The email content
    """
    return f"""
    Bonjour {customer.full_name()},
    Vous avez demandé à réinitialiser votre mot de passe.
    Votre code de réinitialisation est: {customer.reset_password_code}
    Si vous n'êtes pas à l'origine de cette demande, veuillez
    ignorer.
"""


def phone_number_changed(customer: CustomerModel, support_address: str):
    """return email template when a phone number is changed

    Args:
        customer (Customer_model): Customer object
        support_address (str): Support address

        Returns:
            str: The email content
    """
    return f"""
    Bonjour {customer.full_name()},
    Votre numéro de téléphone a bien été modifié.
    Si vous n'êtes pas à l'origine de cette demande, veuillez
    nous contacter à l'adresse {support_address}.
"""


sms_messages = dict(
    {
        SmsConstants.PASSWORD_CHANGED: password_changed,
        SmsConstants.PASSWORD_RESET: password_reset,
        SmsConstants.PHONE_NUMBER_CHANGED: phone_number_changed,
    }
)
