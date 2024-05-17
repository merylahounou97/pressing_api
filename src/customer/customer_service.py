import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from twilio.rest import Client

from src.config import Settings
from src.dependencies.get_api_url import get_api_url
from src.mail import mail_service
from src.person.person_model import Phone_number_model

from ..security import security_service
from . import customer_schema
from .customer_model import Customer_model
from .customer_schema import (Customer_create_input, Customer_edit_input,
                              Customer_verify_code)

settings = Settings()

TWILIO_ACCOUNT_SID = settings.twilio_account_sid
TWILIO_AUTH_TOKEN = settings.twilio_auth_token
TWILIO_PHONE_NUMBER = settings.twilio_phone_number
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def check_existing_customer(db: Session, email: str, phone_number: str):
    """Check if a customer already exists in the database

    Args:
        db (Session): Database session
        email (str): Email of the customer
        phone_number (str): Phone number of the customer

    Returns:
        bool: True if the customer exists, False otherwise
    """
    user = get_customer_by_email_or_phone(db, email, phone_number)
    return user is not None


def get_customer_by_email_or_phone(db: Session, email: str, phone_number: str):
    """Get a customer by email or phone number

    Args:
        db (Session): Database session
        email (str): Email of the customer
        phone_number (str): Phone number of the customer

    Returns:
        Customer_model: Customer object
    """
    return (
        db.query(Customer_model)
        .filter(
            or_(
                Customer_model.phone_number_id == phone_number,
                Customer_model.email == email,
            )
        )
        .first()
    )


async def create_customer(
    db: Session, customerCreate: Customer_create_input, redirect_url: str
):
    """Create a new customer

    Args:
        db (Session): Database session
        customerCreate (Customer_create_input): Customer object
        redirect_url (str): Redirect URL

    Returns:
        Customer_model: Customer object
    """
    if check_existing_customer(
        db, customerCreate.email, customerCreate.phone_number.phone_text
    ):
        raise HTTPException(
            status_code=400, detail="Phone number or email already registered"
        )

    hashed_password = security_service.hashText(customerCreate.password)

    verification_code_email = security_service.generate_random_code()
    verification_code_phone_number = security_service.generate_random_code()
    expiry_time = datetime.now() + timedelta(minutes=settings.code_expiry_time)

    db_user = Customer_model(
        id=str(uuid.uuid4()),
        email=customerCreate.email,
        last_name=customerCreate.last_name,
        first_name=customerCreate.first_name,
        phone_number=Phone_number_model(
            iso_code=customerCreate.phone_number.iso_code,
            dial_code=customerCreate.phone_number.dial_code,
            phone_text=customerCreate.phone_number.phone_text,
        ),
        phone_number_verification_code=verification_code_phone_number,
        email_verification_code=verification_code_email,
        address=customerCreate.address,
        password=hashed_password,
        phone_number_verification_expiry=expiry_time,
        email_verification_expiry=expiry_time,
    )

    db.add(db_user)

    db.commit()

    # Envoyer le SMS de vérification
    twilio_client.messages.create(
        body=f"Votre code de vérification est {verification_code_phone_number}",
        from_=TWILIO_PHONE_NUMBER,
        to=db_user.phone_number_id,
    )

    redirect_url = parse_validation_email(
        redirect_url, verification_code_email, customerCreate.email
    )

    # Send welcome email
    await mail_service.send_welcome_email(customerCreate, redirect_url)

    return db_user


def validate_token(access_token: str, db: Session):
    """Validate the access token

    Args:
        access_token (str): Access token
        db (Session): Database session

    Returns:
        Customer_model: Customer object
    """
    payload = security_service.decode_token(access_token)
    user = get_customer_by_email_or_phone(
        email=payload["sub"], phone_number=payload["phone_number"], db=db
    )
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        return user


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of customers

    Args:
        db (Session): Database session
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Number of records to return. Defaults to 100.

    Returns:
        list[Customer_model]: List of customers
    """
    return db.query(Customer_model).offset(skip).limit(limit).all()


def edit_customer(
    customer_id: str, customer_edit_input: Customer_edit_input, db: Session
):
    """Edit a customer

    Args:
        customer_id (str): Customer ID
        customer_edit_input (Customer_edit_input): Customer edit input
        db (Session): Database session

    Returns:
        Customer_model: Customer object
    """
    db_user = db.query(Customer_model).get({"id": customer_id})
    db_user.last_name = customer_edit_input.last_name
    db_user.first_name = customer_edit_input.first_name
    db_user.address = customer_edit_input.address
    db.commit()
    return db_user


def verify_code(verification: Customer_verify_code, strategy: str, db: Session):
    """Verify the code

    Args:
        verification (Customer_verify_code): Verification object
        strategy (str): Verification strategy
        db (Session): Database session

    Returns:
        Customer_model: Customer object
    """

    if strategy == "email":
        db_user = (
            db.query(Customer_model)
            .filter(
                Customer_model.email == verification.identifier,
                Customer_model.email_verification_code
                == verification.verification_code,
            )
            .first()
        )
        expiry_date_time = db_user.email_verification_expiry

    elif strategy == "phone_number":
        db_user = (
            db.query(Customer_model)
            .filter(
                Customer_model.phone_number_id == verification.identifier,
                Customer_model.phone_number_verification_code
                == verification.verification_code,
            )
            .first()
        )
        expiry_date_time = db_user.phone_number_verification_expiry
    else:
        raise HTTPException(status_code=500, detail="Unknown strategy")

    if not db_user:
        raise HTTPException(status_code=400, detail="Code de vérification invalid")

    if expiry_date_time <= datetime.now():
        setattr(db_user, f"{strategy}_verification_code", None)
        db.commit()
        db.refresh(db_user)
        raise HTTPException(status_code=400, detail="Code de vérification expiré")

    setattr(db_user, f"{strategy}_verified", 1)
    setattr(db_user, f"{strategy}_verification_code", None)

    db.commit()
    db.refresh(db_user)
    return db_user


async def generate_new_validation_code(
    generate_new_validation_code: customer_schema.Customer_generate_new_validation_code_input,
):
    """Generate a new validation code

    Args:
        generate_new_validation_code
           (customer_schema.Customer_generate_new_validation_code_input): Generate new validation
                                                                                    code object

    Returns:
        None
    """
    random_code = security_service.generate_random_code()
    if generate_new_validation_code.strategy == "email":
        generate_new_validation_code.redirect_url = parse_validation_email(
            generate_new_validation_code.redirect_url,
            random_code,
            generate_new_validation_code.identifier,
        )
    await mail_service.send_welcome_email(
        generate_new_validation_code, generate_new_validation_code.redirect_url
    )


def parse_validation_email(redirect_url: str, verification_code_email: str, email: str):
    """Parse the validation email

    Args:
        redirect_url (str): Redirect URL
        verification_code_email (str): Verification code
        email (str): Email

    Returns:
        str: Redirect URL
    """
    if settings.ENV == "dev":
        redirect_url = get_api_url()
    return f"{redirect_url}?code={verification_code_email}&identifier={email}"
