from sqlalchemy.orm import Session


from ..customer.customer_model import CustomerModel


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
        .filter(CustomerModel.phone_number.phone_text == phone_number)
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


