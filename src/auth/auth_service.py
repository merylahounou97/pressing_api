from sqlalchemy.orm import Session

from src.customer import customer_service

from ..customer.customer_model import CustomerModel
from ..security import security_service


def get_user_by_email(db: Session, email: str):
    """Get a user by email

    args:
        db (Session): The database session
        email (str): The email

    Returns:
        Customer_model: The user
    """
    return db.query(CustomerModel).filter(CustomerModel.email == email).first()


def get_user_by_tel_number(db: Session, phone_number: str):
    """Get a user by phone number

    args:
        db (Session): The database session
        phone_number (str): The phone number

    Returns:
        Customer_model: The user
    """
    return (
        db.query(CustomerModel)
        .filter(CustomerModel.phone_number_id == phone_number)
        .first()
    )


def get_user_by_identifier(db: Session, identifier: str):
    """Get a user by identifier

    args:
        db (Session): The database session
        identifier (str): The identifier

    Returns:
        Customer_model: The user
    """
    user = get_user_by_email(db, identifier)
    if not user:
        return get_user_by_tel_number(db, identifier)
    else:
        return user


# Créer une fonction pour vérifier les informations de connexion
def authenticate_user(db: Session, identifier: str, password: str):
    """Authenticate a user by email or phone number

    args:
        db (Session): The database session
        identifier (str): The identifier
        password (str): The password

    Returns:
        Customer_model: The user
    """
    user = customer_service.get_customer_by_email_or_phone(
        db=db, email=identifier, phone_number=identifier
    )
    if user is not None and security_service.compare_hashed_text(
        password, user.password
    ):
        return user
