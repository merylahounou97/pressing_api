from src.utils.sms_constants import SmsConstants
from src.users.user_model import UserModel

def password_changed(user: UserModel, support_address: str):
    """return email template when a password is changed

    Args:
        user (User_model): User object
        support_address (str): Support address

        Returns:
            str: The email content
    """
    return f"""
    Bonjour {user.first_name},
    Votre mot de passe a bien été modifié.
    Merci de vous reconnecter avec votre nouveau mot de passe.
    Si vous n'êtes pas à l'origine de cette demande, veuillez
    nous contacter à l'adresse {support_address}.
"""


def password_reset(user: UserModel):
    """return email template when a password is reset

    Args:
        user (User_model): User object
        support_address (str): Support address

        Returns:
            str: The email content
    """
    return f"""
    Bonjour {user.full_name()},
    Vous avez demandé à réinitialiser votre mot de passe.
    Votre code de réinitialisation est: {user.reset_password_code}
    Si vous n'êtes pas à l'origine de cette demande, veuillez
    ignorer.
"""


def phone_number_changed(user: UserModel, support_address: str):
    """return email template when a phone number is changed

    Args:
        user (User_model): User object
        support_address (str): Support address

        Returns:
            str: The email content
    """
    return f"""
    Bonjour {user.full_name},
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
