from enum import Enum

from pydantic import BaseModel, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber


class ValidationStrategyEnum(Enum):
    """Stratégie de validation"""

    PHONE_NUMBER = "phone_number"
    EMAIL = "email"


class PhoneNumberModel(BaseModel):
    """Modèle de numéro de téléphone
    Attributes:
        iso_code (str): Code ISO du pays
        dial_code (str): Code de composition du numéro
        phone_text (PhoneNumber): Numéro de téléphone
    """

    iso_code: str
    dial_code: str
    phone_text: PhoneNumber

    # Ajout d'une méthode de validation personnalisée pour `phone_text`
    @field_validator("phone_text")
    def remove_tel_prefix(self, v):
        """Supprime le préfixe 'tel:' et les tirets du numéro de téléphone
        Args:
            v (PhoneNumber): Numéro de téléphone

        Returns:
            PhoneNumber: Numéro de téléphone sans préfixe 'tel:' et sans tirets
        """
        return PhoneNumber.removeprefix(v, "tel:").replace("-", "")


class PersonInputBase(BaseModel):
    """Modèle de base pour les informations d'une personne
    Attributes:
        last_name (str): Nom de famille
        first_name (str): Prénom
        address (str): Adresse
        email (EmailStr): Adresse email
        phone_number (PhoneNumberModel): Numéro de téléphone
    """

    last_name: str
    first_name: str
    address: str
    email: EmailStr
    phone_number: PhoneNumberModel


class Person(PersonInputBase):
    """Modèle de personne
    Attributes:
        id (str): Identifiant unique de la personne
        phone_number_verified (bool): Indique si le numéro de téléphone a été vérifié
        email_verified (bool): Indique si l'adresse email a été vérifiée
    """

    phone_number_verified: bool
    email_verified: bool


class PersonVerificationInput(BaseModel):
    """Modèle de vérification d'une personne
    Attributes:
        identifier (str): Identifiant de la personne
        verification_code (str): Code de vérification
    """

    identifier: str
    verification_code: str


class PersonGenerateNewvalidationCodeInput(BaseModel):
    """Modèle de génération d'un nouveau code de validation
    Attributes:
        identifier (str): Identifiant de la personne
        strategy (ValidationStrategyEnum): Stratégie de validation
        redirect_url (str): URL de redirection
    """

    identifier: str
    strategy: ValidationStrategyEnum
    redirect_url: str
