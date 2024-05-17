from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.config import Settings
from src.customer import customer_schema, customer_service
from src.customer.customer_schema import (
    Customer_create_input,
    Customer_edit_input,
    Customer_output,
    Customer_verify_code,
)
from src.dependencies.db import get_db

from ..security import security_service

settings = Settings()

router = APIRouter(prefix="/customers")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


access_token_dep = Annotated[str, Depends(oauth2_scheme)]


@router.post("/", response_model=Customer_output)
async def create_customers(
    customer: Customer_create_input, redirect_url: str, db: Session = Depends(get_db)
):
    return await customer_service.create_customer(db, customer, redirect_url)


@router.get("/", response_model=list[Customer_output])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = customer_service.get_customers(db=db, skip=skip, limit=limit)
    return users


@router.patch("/", response_model=Customer_output)
def edit_customer(
    customer_edit_input: Customer_edit_input,
    access_token: access_token_dep,
    db: Session = Depends(get_db),
):
    user = customer_service.validate_token(access_token=access_token, db=db)
    return customer_service.edit_customer(
        id=user.id, customer_edit_input=customer_edit_input, db=db
    )


@router.post("/verify_phone_number/")
def verify_code(verification: Customer_verify_code, db: Session = Depends(get_db)):
    return customer_service.verify_code(
        verification=verification, db=db, strategy="phone_number"
    )


@router.post("/verify_email")
def verify_email(verification: Customer_verify_code, db: Session = Depends(get_db)):
    return customer_service.verify_code(
        verification=verification, db=db, strategy="email"
    )


@router.post("/generate_new_email_validation_code")
def generate_new_email_validation_code(
    create_new_validation_code_input: customer_schema.Customer_generate_new_validation_code_input,
):
    return customer_service.generate_new_validation_code(
        create_new_validation_code_input
    )
