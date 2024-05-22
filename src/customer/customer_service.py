import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.config import Settings
from src.mail import mail_service
from src.mail.mail_service import parse_validation_email
from src.person.person_model import PhoneNumber
from src.sms import sms_service

from ..security import security_service
from . import customer_schema
from .customer_model import CustomerModel
from ..person import person_schema
from .customer_schema import (
    CreateCustomerInput,
    CustomerEditInput,
    CustomerValidationCode,
)

settings = Settings()



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
        db.query(CustomerModel)
        .filter(
            or_(
                CustomerModel.phone_number_id == phone_number,
                CustomerModel.email == email,
            )
        )
        .first()
    )


async def create_customer(
    db: Session, customer_create: CreateCustomerInput, redirect_url: str
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
        db, customer_create.email, customer_create.phone_number.phone_text
    ):
        raise HTTPException(
            status_code=400, detail="Phone number or email already registered"
        )

    hashed_password = security_service.hash_text(customer_create.password)

    verification_code_email = security_service.generate_random_code()
    verification_code_phone_number = security_service.generate_random_code()
    expiry_time = datetime.now() + timedelta(minutes=settings.code_expiry_time)

    db_user = CustomerModel(
        id=str(uuid.uuid4()),
        email=customer_create.email,
        last_name=customer_create.last_name,
        first_name=customer_create.first_name,
        phone_number=PhoneNumber(
            iso_code=customer_create.phone_number.iso_code,
            dial_code=customer_create.phone_number.dial_code,
            phone_text=customer_create.phone_number.phone_text,
        ),
        phone_number_verification_code=verification_code_phone_number,
        email_verification_code=verification_code_email,
        address=customer_create.address,
        password=hashed_password,
        phone_number_verification_expiry=expiry_time,
        email_verification_expiry=expiry_time,
    )

    db.add(db_user)

    db.commit()

    # Envoyer le SMS de vérification
    sms_service.send_welcome_sms(db_user)

    # Send welcome email
    await mail_service.send_welcome_email(customer_create, redirect_url)

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
    return db.query(CustomerModel).offset(skip).limit(limit).all()


def edit_customer(
    customer_id: str, customer_edit_input: CustomerEditInput, db: Session
):
    """Edit a customer

    Args:
        customer_id (str): Customer ID
        customer_edit_input (Customer_edit_input): Customer edit input
        db (Session): Database session

    Returns:
        Customer_model: Customer object
    """
    db_user = db.query(CustomerModel).get({"id": customer_id})
    db_user.last_name = customer_edit_input.last_name
    db_user.first_name = customer_edit_input.first_name
    db_user.address = customer_edit_input.address
    db.commit()
    return db_user


def verify_code(verification: CustomerValidationCode, strategy: str, db: Session):
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
            db.query(CustomerModel)
            .filter(
                CustomerModel.email == verification.identifier,
                CustomerModel.email_verification_code == verification.verification_code,
            )
            .first()
        )
        expiry_date_time = db_user.email_verification_expiry

    elif strategy == "phone_number":
        db_user = (
            db.query(CustomerModel)
            .filter(
                CustomerModel.phone_number_id == verification.identifier,
                CustomerModel.phone_number_verification_code
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
    new_validation_code: customer_schema.CustomerNewValidationCodeInput,
    db
):
    """Generate a new validation code

    Args:
        generate_new_validation_code
           (customer_schema.Customer_generate_new_validation_code_input): Generate new validation
                                                                                    code object

    Returns:
        None
    """
    print("generate_new_validation_code")
    random_code = security_service.generate_random_code()

    user =  get_customer_by_email_or_phone(db=db,
                                          email=new_validation_code.identifier,
                                          phone_number=new_validation_code.identifier
                                        )

    if new_validation_code.strategy == person_schema.ValidationStrategyEnum.EMAIL:
        print("1")
        new_validation_code.redirect_url = parse_validation_email(
            new_validation_code.redirect_url,
            random_code,
            new_validation_code.identifier,
        )
    
        await mail_service.send_validation_email(person=user, redirect_url=new_validation_code.redirect_url)
    elif (
        new_validation_code.strategy
        == person_schema.ValidationStrategyEnum.PHONE_NUMBER
    ):
        print("2")
        sms_service.send_verification_sms(new_validation_code.identifier, random_code)
    else:
        print("3")
        raise HTTPException(status_code=400, detail="Unknown strategy")
