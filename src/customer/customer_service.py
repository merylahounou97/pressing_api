from typing import Union
import uuid
from datetime import datetime, timedelta

from pydantic import EmailStr

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.config import Settings
from src.customer import customer_service
from src.dependencies.get_api_url import get_api_url
from src.mail import mail_service
from src.mail.mail_service import parse_validation_email
from src.security import security_service
from src.sms import sms_service
from src.utils.functions import get_identifier_type
from src.utils.mail_constants import MailConstants
from src.utils.sms_constants import SmsConstants
from pydantic_extra_types.phone_numbers import  PhoneNumber

from ..security import security_service
from .customer_model import CustomerModel
from ..person import person_schema
from .customer_schema import (
    CreateCustomerInput,
)

settings = Settings()


def check_existing_customer(db: Session, identifier : Union[EmailStr, PhoneNumber]):
    """Check if a customer already exists in the database

    Args:
        db (Session): Database session
        email (str): Email of the customer
        phone_number (str): Phone number of the customer

    Returns:
        bool: True if the customer exists, False otherwise
    """
    user = get_customer_by_identifier(db, identifier)
    return user is not None


def get_customer_by_id(customer_id, db: Session):
    """Get a customer by id

    Args:
        db (Session): Database session
        customer_id (str): Customer id

    Returns:
        Customer_model: Customer object
    """
    return db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()




def get_customer_by_identifier(
    db: Session, identifier: str
) -> CustomerModel | None:
    """Get a customer by email or phone number

    Args:
        db (Session): Database session
        email (str): Email of the customer
        phone_number (str): Phone number of the customer

    Returns:
        Customer_model: Customer object or null
    """
    return db.query(CustomerModel).filter(or_(CustomerModel.phone_number==identifier,CustomerModel.email==identifier)).first() 


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

    if customer_create.phone_number is None and customer_create.email is None:
        raise HTTPException(
            status_code=400, detail="Phone number and email cannot be both empty"
        )

    try:
        hashed_password = security_service.hash_text(customer_create.password)

        verification_code_email = security_service.generate_random_code()
        verification_code_phone_number = security_service.generate_random_code()
        expiry_time = datetime.now() + timedelta(minutes=settings.code_expiry_time)

        user_id = (str(uuid.uuid4()),)
        db_user = CustomerModel(
            id=user_id,
            email=customer_create.email,
            phone_number = customer_create.phone_number,
            last_name=customer_create.last_name,
            first_name=customer_create.first_name,
            phone_number_verification_code=verification_code_phone_number,
            email_verification_code=verification_code_email,
            address=customer_create.address,
            password=hashed_password,
            phone_number_verification_expiry=expiry_time,
            email_verification_expiry=expiry_time,
        )

        db.add(db_user)

        db.commit()

        # Send welcome email
        if customer_create.email is not None:
            api_url = get_api_url()
            redirect_url = mail_service.parse_validation_email(
                redirect_url, db_user.email_verification_code, db_user.email
            )
            mail_service.send_mail_from_template(
                MailConstants.WECOME_EMAIL,
                db_user.email,
                redirect_url=redirect_url,
                app_name=settings.app_name,
                person=db_user,
                api_url=api_url,
            )

        if customer_create.phone_number is not None:
            # Envoyer le SMS de vérification
            sms_service.send_welcome_sms(db_user)

        return db_user
    except Exception as e:
        is_unique_violation = str(e).count("psycopg2.errors.UniqueViolation") == 1
        if is_unique_violation:
            raise HTTPException(
                status_code=400, detail="Phone number or email already registered"
            )
        raise HTTPException(status_code=400, detail=str(e))


def validate_token(access_token: str, db: Session):
    """Validate the access token

    Args:
        access_token (str): Access token
        db (Session): Database session

    Returns:
        Customer_model: Customer object
    """
    payload = security_service.decode_token(access_token)
    user = get_customer_by_id(payload["sub"], db)
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


def set_new_email(customer_online: CustomerModel, email: str):
    """Set a new email for a customer
    Change the email of the customer and generate a new verification code for the new email.
    put the new email to non verified
    and add the expiration of the verification code

    Args:
        customer_online (Customer_model): Customer object
        email (str): New email

        Returns:
            Customer_model: Customer object
    """
    customer_online.email = email
    customer_online.email_verification_code = security_service.generate_random_code()
    customer_online.email_verification_expiry = datetime.now() + timedelta(
        minutes=settings.code_expiry_time
    )
    customer_online.email_verified = 0
    return None


def set_new_phone_number(customer_online: CustomerModel, phone_number: str):
    customer_online.phone_number = phone_number
    customer_online.phone_number_verification_code = (
        security_service.generate_random_code()
    )
    customer_online.phone_number_verification_expiry = datetime.now() + timedelta(
        minutes=settings.code_expiry_time
    )
    customer_online.phone_number_verified = 0
    return None


def edit_customer(
    customer_online: CustomerModel,
    customer_edit_input: person_schema.PersonBaseSchema,
    db: Session,
):
    """Edit a customer

    Args:
        customer_id (str): Customer ID
        customer_edit_input (Customer_edit_input): Customer edit input
        db (Session): Database session

    Returns:
        Customer_model: Customer object
    """

    customer_old_mail = customer_online.email
    if customer_edit_input.last_name is not None:
        customer_online.last_name = customer_edit_input.last_name
    if customer_edit_input.first_name is not None:
        customer_online.first_name = customer_edit_input.first_name
    if customer_edit_input.address is not None:
        customer_online.address = customer_edit_input.address

    if (
        customer_edit_input.email is not None
        and customer_edit_input.email != customer_online.email
    ):
        set_new_email(customer_online, customer_edit_input.email)

    if (
        customer_edit_input.phone_number is not None
        and customer_edit_input.phone_number != customer_online.phone_number
    ):
        set_new_phone_number(customer_online, customer_edit_input.phone_number)

    db.commit()

    # Sent email if it has been changed
    if (
        customer_edit_input.email is not None
        and customer_edit_input.email != customer_old_mail
    ):
        mail_service.send_mail_from_template(
            MailConstants.UPDATE_EMAIL,
            email=customer_edit_input.email,
            customer=customer_online,
            redirect_url="google.com",
        )

    # Send SMS if it has been changed
    if (
        customer_edit_input.phone_number is not None
        and customer_edit_input.phone_number != customer_online.phone_number
    ):
        sms_service.send_sms(
            customer_online.phone_number,
            template_name=SmsConstants.PHONE_NUMBER_CHANGED,
            customer=customer_online,
            support_address=settings.support_address,
        )

    return customer_online


def verify_code(verification: person_schema.VerifyIdentifierInput, db: Session):
    """Verify the code

    Args:
        verification (Customer_verify_code): Verification object
        strategy (str): Verification strategy
        db (Session): Database session

    Returns:
        Customer_model: Customer object
    """

    strategy = get_identifier_type(verification.identifier)

    strategy_string = strategy.name.lower()

    if strategy == person_schema.IdentifierEnum.EMAIL:
        db_user = (
            db.query(CustomerModel)
            .filter(
                CustomerModel.email == verification.identifier,
                CustomerModel.email_verification_code == verification.verification_code,
            )
            .first()
        )

        if db_user is not None:
            expiry_date_time = db_user.email_verification_expiry

    elif strategy == person_schema.IdentifierEnum.PHONE_NUMBER:
        db_user = (
            db.query(CustomerModel)
            .filter(
                CustomerModel.phone_number == verification.identifier,
                CustomerModel.phone_number_verification_code
                == verification.verification_code,
            )
            .first()
        )
        if db_user is not None:
            expiry_date_time = db_user.phone_number_verification_expiry
    else:
        raise HTTPException(status_code=500, detail="Unknown strategy")

    if not db_user:
        raise HTTPException(status_code=400, detail="Code de vérification invalid")

    if expiry_date_time <= datetime.now():
        setattr(db_user, f"{strategy_string}_verification_code", None)
        db.commit()
        db.refresh(db_user)
        raise HTTPException(status_code=400, detail="Code de vérification expiré")

    setattr(db_user, f"{strategy_string}_verified", 1)
    setattr(db_user, f"{strategy_string}_verification_code", None)

    db.commit()
    db.refresh(db_user)
    return db_user


async def generate_new_validation_code(
    new_validation_code: person_schema.ResetAndValidationInput, db
):
    """Generate a new validation code

    Args:
        generate_new_validation_code
           (customer_schema.Customer_generate_new_validation_code_input): Generate new validation
                                                                                    code object

    Returns:
        None
    """

    strategy = (
        person_schema.IdentifierEnum.EMAIL
        if new_validation_code.identifier.count("@") == 1
        else person_schema.IdentifierEnum.PHONE_NUMBER
    )

    user = get_customer_by_identifier(db,new_validation_code.identifier )

    if user is not None:
        random_code = security_service.generate_random_code()

        if strategy == person_schema.IdentifierEnum.EMAIL and not user.email_verified:
            set_new_email(user, user.email)
            db.commit()
            db.refresh(user)

            new_validation_code.redirect_url = parse_validation_email(
                new_validation_code.redirect_url,
                random_code,
                new_validation_code.identifier,
            )

            redirect_url = mail_service.parse_validation_email(
                redirect_url=new_validation_code.redirect_url,
                verification_code_email=random_code,
                email=user.email,
            )
            mail_service.send_mail_from_template(
                MailConstants.EMAIL_VERIFICATION,
                email=user.email,
                person=user,
                redirect_url=redirect_url,
            )

            return user
        elif (
            strategy == person_schema.IdentifierEnum.PHONE_NUMBER
            and not user.phone_number_verified
        ):
            user.phone_number_verification_code = random_code
            user.phone_number_verification_expiry = datetime.now() + timedelta(
                minutes=settings.code_expiry_time
            )

            db.commit()
            db.refresh(user)

            sms_service.send_verification_sms(
                new_validation_code.identifier, random_code
            )
            return user
        elif user.phone_number_verified or user.email_verified:
            return None
        else:
            raise HTTPException(status_code=400, detail="Unknown strategy")
    return None


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
    user = customer_service.get_customer_by_identifier(db, identifier)
    if user is not None and security_service.compare_hashed_text(
        password, user.password
    ):
        return user


def change_password(
    customer_online: CustomerModel,
    change_password_input: person_schema.ChangePersonPassword,
    db: Session,
):
    """Change the password

    Args:
        customer_online (Customer_model): Customer object
        change_password_input (Customer_change_password_input): Change password input
        db (Session): Database session

        Returns:
            Customer_model: Customer object
    """

    if not (
        customer_online.is_valid_email() or customer_online.is_valid_phone_number()
    ):
        raise HTTPException(
            status_code=400, detail="Email or phone number should be verified"
        )

    if change_password_input.old_password == change_password_input.new_password:
        raise HTTPException(
            status_code=400, detail="New password should be different from the old one"
        )

    if security_service.compare_hashed_text(
        change_password_input.old_password, customer_online.password
    ):
        customer_online.password = security_service.hash_text(
            change_password_input.new_password
        )
        db.commit()

        if customer_online.is_valid_phone_number():
            sms_service.send_sms(
                customer_online.phone_number.phone_text,
                template_name=SmsConstants.PASSWORD_CHANGED,
                customer=customer_online,
                support_address=settings.support_address,
            )

        if customer_online.is_valid_email():
            mail_service.send_mail_from_template(
                MailConstants.PASSWORD_CHANGED,
                email=customer_online.email,
                customer=customer_online,
                support_address=settings.support_address,
            )
        return customer_online

    else:
        raise HTTPException(status_code=400, detail="Wrong old password")


def reset_password(identifier: str, db: Session):
    """Reset the password

    Args:
        identifier (str): The identifier
        db (Session): Database session

    Returns:
        Customer_model: The user
    """

    user = get_customer_by_identifier(db, identifier)

    if user is None:
        raise HTTPException(status_code=400, detail="User not found")

    random_code = security_service.generate_random_code()
    user.reset_password_code = random_code
    db.commit()

    strategy = get_identifier_type(identifier)
    if strategy == person_schema.IdentifierEnum.EMAIL and user.email is not None:
        mail_service.send_mail_from_template(
            MailConstants.PASSWORD_RESET, email=user.email, customer=user
        )
    elif (
        strategy == person_schema.IdentifierEnum.PHONE_NUMBER
        and user.phone_number is not None
    ):
        sms_service.send_sms(
            user.phone_number.phone_text,
            template_name=SmsConstants.PASSWORD_RESET,
            customer=user,
        )
    else:
        raise HTTPException(status_code=500, detail="Invalid user identifier")

    return user


def submit_reset_password(reset_input: person_schema.ResetPasswordInput, db: Session):
    """Submit the reset password

    Args:
        reset_input (ResetPasswordInput): The reset input
        db (Session): Database session

    Returns:
        Customer_model: The user
    """
    user = get_customer_by_identifier(db, reset_input.identifier)
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")

    if user.reset_password_code != reset_input.verification_code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    user.password = security_service.hash_text(reset_input.new_password)
    user.reset_password_code = None
    db.commit()

    return user
