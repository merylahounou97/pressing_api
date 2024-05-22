from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.config import Settings
from src.customer import customer_schema, customer_service
from src.customer.customer_schema import (CreateCustomerInput,
                                          CustomerEditInput, CustomerOutput,
                                          CustomerValidationCode)
from src.dependencies.db import get_db

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


@router.get("/", response_model=list[CustomerOutput])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get customers from the database

    Args:
        skip (int, optional): The skip. Defaults to 0.
        limit (int, optional): The limit. Defaults to 100.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        list[Customer_output]: The list of customers
    """
    users = customer_service.get_customers(db=db, skip=skip, limit=limit)
    return users


@router.patch("/", response_model=CustomerOutput)
def edit_customer(
    customer_edit_input: CustomerEditInput,
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
        customer_id=user.id, customer_edit_input=customer_edit_input, db=db
    )


@router.post("/verify_phone_number/")
def verify_code(verification: CustomerValidationCode, db: Session = Depends(get_db)):
    """Verify a phone number by code

    Args:
        verification (Customer_verify_code): The verification code
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        bool: The verification result
    """
    return customer_service.verify_code(
        verification=verification, db=db, strategy="phone_number"
    )


@router.post("/verify_email")
def verify_email(verification: CustomerValidationCode, db: Session = Depends(get_db)):
    """Verify an email by code

    Args:
        verification (Customer_verify_code): The verification code
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        bool: The verification result
    """
    return customer_service.verify_code(
        verification=verification, db=db, strategy="email"
    )


@router.post("/validate_identifier")
async def generate_new_email_validation_code(
    create_new_validation_code_input: customer_schema.CustomerNewValidationCodeInput,
     db: Session = Depends(get_db)):
    """Generate a new email validation code

    Args:
        create_new_validation_code_input (Customer_generate_new_validation_code_input): The input

    Returns:
        bool: The result
    """
    return await customer_service.generate_new_validation_code(db=db,
        new_validation_code=create_new_validation_code_input
    )
