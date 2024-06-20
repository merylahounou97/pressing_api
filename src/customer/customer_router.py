from typing import Union
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.config import Settings
from src.customer import customer_service
from src.customer.customer_model import CustomerModel
from src.customer.customer_schema import CreateCustomerInput, CustomerOutput
from src.dependencies.db import get_db
from src.person.person_schema import (
    ChangePersonPassword,
    PersonBaseSchema,
    ResetPasswordInput,
    VerifyIdentifierInput,
)

from src.dependencies.get_customer_online import get_customer_online

settings = Settings()

router = APIRouter(prefix="/customers")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


AccessTokenDep = Annotated[str, Depends(oauth2_scheme)]


@router.post("/", response_model=CustomerOutput)
async def create_customers(
    customer: CreateCustomerInput, redirect_url: str, db: Session = Depends(get_db)
):
    """Create a customer

    Args:
        customer (Customer_create_input): The customer input
        redirect_url (str): The redirect url
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Customer_output: The customer output
    """
    return await customer_service.create_customer(db, customer, redirect_url)


@router.patch("/", response_model=Union[CustomerOutput, None])
async def edit_customer(
    customer_edit_input: PersonBaseSchema,
    access_token: AccessTokenDep,
    db: Session = Depends(get_db),
):
    """Edit a customer by id

    Args:
        customer_edit_input (Customer_edit_input): The customer edit input
        access_token (access_token_dep): The access token
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Customer_output: The customer output
    """
    user = customer_service.validate_token(access_token=access_token, db=db)
    return customer_service.edit_customer(
        customer_online=user, customer_edit_input=customer_edit_input, db=db
    )


@router.post("/verify_verification_code", response_model=CustomerOutput)
async def verify_verification_code(
    customer_validation_code: VerifyIdentifierInput, db: Session = Depends(get_db)
):
    """Verify a phone number by code

    Args:
        verification (Customer_verify_code): The verification code
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        bool: The verification result
    """
    return customer_service.verify_code(verification=customer_validation_code, db=db)


@router.post("/send_verification_code", response_model=Union[CustomerOutput, None])
async def generate_new_email_validation_code(
    identifier: Annotated[str, Body(embed=True)] , db: Session = Depends(get_db)
):
    """Generate a validation code sent to the user by email or phone number

    Args:
        identifier: email or phone number

    Returns:
        bool: The result
    """
    return await customer_service.generate_new_validation_code(identifier=identifier, db=db)


@router.patch("/change_password", response_model=CustomerOutput)
def change_password(
    change_password_input: ChangePersonPassword,
    user_online: CustomerModel = Depends(get_customer_online),
    db: Session = Depends(get_db),
):
    """A router to Change a customer password

    Args:
        change_password_input (Change_password_input): The change password input
        user_online (Customer_model, optional): The user online. Defaults to Depends(get_customer_online).
        db (Session, optional): The database session. Defaults to Depends(get_db).

        Returns:
            Customer_output: The customer output
    """

    return customer_service.change_password(user_online, change_password_input, db=db)


@router.patch("/reset_password", response_model=CustomerOutput)
def reset_password(identifier: str, db: Session = Depends(get_db)):
    """A router to reset a customer password

    Args:

        identifier (str): The customer identifier can be email or phone number
        db (Session, optional): The database session. Defaults to Depends(get_db).


        Returns:
            Customer_output: The customer output"""
    identifier = identifier.replace(" ", "")
    return customer_service.reset_password(identifier, db=db)


@router.patch("/submit_reset_password", response_model=CustomerOutput)
def submit_reset_password(
    reset_input: ResetPasswordInput, db: Session = Depends(get_db)
):
    """A router to submit a new password

    Args:

        reset_input (VerifyIdentifierInput): The reset input
        db (Session, optional): The database session. Defaults to Depends(get_db).


        Returns:
            Customer_output: The customer output"""
    return customer_service.submit_reset_password(reset_input, db=db)
