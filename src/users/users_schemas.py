from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from src.users.users_model import UserRole

class IdentifierEnum(Enum):
    """Stratégie de validation"""

    PHONE_NUMBER = "phone_number"
    EMAIL = "email"


class UserBaseSchema(BaseModel):
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
    phone_number: Optional[PhoneNumber] = None

    @field_validator("phone_number")
    @classmethod
    def remove_tel_prefix(cls, v):
        """Supprime le préfixe 'tel:' et les tirets du numéro de téléphone
        Args:
            v (PhoneNumber): Numéro de téléphone

        Returns:
            PhoneNumber: Numéro de téléphone sans préfixe 'tel:' et sans tirets
        """
        return (
            PhoneNumber.removeprefix(v, "tel:").replace("-", "").replace(" ", "")
            if v is not None
            else None
        )


class UserSchema(UserBaseSchema):
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

class ChangeUserPassword(BaseModel):
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


class UserCreateInput(UserBaseSchema):
    """Create customer input model

    Attributes:
        password (str): The password of the customer
    """
    password: str

class UserCreateMemberInput(UserCreateInput):
    """Create member (secretary or admin) input model

    Attributes:
        role (UserRole): The role of the member
    """
    role: UserRole

class UserOutput(UserSchema,UserCreateMemberInput):
    """User output of any user
    Attributes:
        id (int): The customer id
        first_name (str): The first name of the customer
        last_name (str): The last name of the customer
        email (str): The email of the customer
        phone_number (str): The phone number of the customer
        address (str): The address of the customer
        is_active (bool): The status of the customer
        is_verified (bool): The verification status of the customer
    """
    id: str

class UserQueryOptions(UserSchema):
    """User query options
    Attributes:
        limit (int): The limit of the query
        offset (int): The offset of the query
    """
    role: Optional[UserRole]=None
    email_verified: Optional[bool]=None
    phone_number_verified: Optional[bool]=None
    limit: int=30
    offset: int=0