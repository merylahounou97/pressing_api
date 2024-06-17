from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber


class IdentifierEnum(Enum):
    """Stratégie de validation"""

    PHONE_NUMBER = "phone_number"
    EMAIL = "email"


class PhoneNumberSchema(BaseModel):
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
    def remove_tel_prefix(cls, v):
        """Supprime le préfixe 'tel:' et les tirets du numéro de téléphone
        Args:
            v (PhoneNumber): Numéro de téléphone

        Returns:
            PhoneNumber: Numéro de téléphone sans préfixe 'tel:' et sans tirets
        """
        return PhoneNumber.removeprefix(v, "tel:").replace("-", "").replace(" ", "")


class PersonBaseSchema(BaseModel):
    """Modèle de base pour les informations d'une personne
    Attributes:
        last_name (str): Nom de famille
        first_name (str): Prénom
        address (str): Adresse
        email (EmailStr): Adresse email
        phone_number (PhoneNumberModel): Numéro de téléphone
    """

    last_name: Optional[str] = None
    first_name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[PhoneNumberSchema] = None


class PersonBaseSchemaCreate(PersonBaseSchema):
    email_redirect_url: Optional[str] = None
    phone_number_redirect_url: Optional[str] = None


class PersonSchema(PersonBaseSchema):
    """Modèle de personne
    Attributes:
        id (str): Identifiant unique de la personne
        phone_number_verified (bool): Indique si le numéro de téléphone a été vérifié
        email_verified (bool): Indique si l'adresse email a été vérifiée
    """

    phone_number_verified: bool
    email_verified: bool


class VerifyIdentifierInput(BaseModel):
    """Modèle de vérification d'une personne
    Attributes:
        identifier (str): Identifiant de la personne
        verification_code (str): Code de vérification
    """

    identifier: str
    verification_code: str


class ResetAndValidationInput(BaseModel):
    """Modèle de génération d'un nouveau code de validation
    Attributes:
        identifier (str): Identifiant de la personne
        strategy (ValidationStrategyEnum): Stratégie de validation
        redirect_url (str): URL de redirection
    """

    identifier: str
    redirect_url: str


class ChangePersonPassword(BaseModel):
    """Modèle de changement de mot de passe
    Attributes:
        old_password (str): Ancien mot de passe
        new_password (str): Nouveau mot de passe
    """

    old_password: str
    new_password: str


class ResetPasswordInput(VerifyIdentifierInput):
    """Modèle de réinitialisation du mot de passe
    Attributes:
        new_password (str): Nouveau mot de passe
    """

    new_password: str
