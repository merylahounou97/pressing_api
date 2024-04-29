
from sqlalchemy.orm import Session
from sql.customer.customer_model import Customer_model



def get_user_by_email(db: Session, email: str):
    return db.query(Customer_model).filter(Customer_model.email == email).first()


def get_user_by_tel_number(db: Session, phone_number: str):
    return db.query(Customer_model).filter(Customer_model.phone_number == phone_number).first()


def get_user_by_identifier(db: Session, identifier :str):
    """
    
    """
    user = get_user_by_email(db, identifier)
    if not user :
        return get_user_by_tel_number(db, identifier)


# Créer une fonction pour vérifier les informations de connexion
def authenticate_user(db: Session, identifier: str, password: str):
    """
    
    """
    user = get_user_by_identifier(db, identifier)
    if not user or user.password != password:
        return False
    #Prévoir le message d'erreur
    return user