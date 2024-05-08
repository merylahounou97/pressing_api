from sqlalchemy.orm import Session

from src.customer import customer_service
from ..customer.customer_model import Customer_model
from ..security import security_service


def get_user_by_email(db: Session, email: str):
    return db.query(Customer_model).filter(Customer_model.email == email).first()

def get_user_by_tel_number(db: Session, phone_number: str):
    return db.query(Customer_model).filter(Customer_model.phone_number_id == phone_number).first()


def get_user_by_identifier(db: Session, identifier :str):
    """
    
    """
    user = get_user_by_email(db, identifier)
    if not user :
        return get_user_by_tel_number(db, identifier)
    else:
        return user


# Créer une fonction pour vérifier les informations de connexion
def authenticate_user(db: Session, identifier: str, password: str):
    """
    
    """
    user = customer_service.get_customer_by_email_or_phone(db=db,email=identifier,phone_number=identifier)
    if user is not None and security_service.compareHashedText(password,user.password):
        return user
    else:
        return None