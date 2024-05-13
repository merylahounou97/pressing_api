
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.mail import mail_service
from src.person.person_model import Phone_number_model
from src.person.person_schema import Phone_number
from .customer_model import Customer_model
from .customer_schema import  Customer_create_input,Customer_edit_input
import uuid
from fastapi import Depends, HTTPException
from src.dependencies.db import get_db

from ..security import security_service 



def check_existing_customer(db: Session, email: str, phone_number: str):
    user = get_customer_by_email_or_phone(db, email, phone_number)
    return user is not None

def get_customer_by_email_or_phone(db: Session, email: str, phone_number: str):
    return db.query(Customer_model).filter( or_(Customer_model.phone_number_id == phone_number, Customer_model.email == email)  ).first()


async def create_customer(db: Session, customerCreate: Customer_create_input):
    if check_existing_customer(db, customerCreate.email, customerCreate.phone_number.phone_text):
        raise HTTPException(status_code=400, detail="Phone number or email already registered")
    
    hashed_password = security_service.hashText(customerCreate.password)

    db_user = Customer_model(
        id= str(uuid.uuid4()),
        email =customerCreate.email,
        last_name =customerCreate.last_name,
        first_name =customerCreate.first_name,
        phone_number =Phone_number_model(
        iso_code= customerCreate.phone_number.iso_code,
        dial_code= customerCreate.phone_number.dial_code,
        phone_text= customerCreate.phone_number.phone_text,
    ),
        address =customerCreate.address,
        password =hashed_password 
    )

    db.add(db_user)
    
    db.commit()

    
    #Send welcome email
    await mail_service.send_welcome_email(customerCreate)

    return db_user


def validate_token(access_token:str, db: Session):
    payload = security_service.decode_token(access_token)
    user = get_customer_by_email_or_phone(email=payload["sub"],phone_number=payload["phone_number"],db=db)
    if  user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
         return user

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer_model).offset(skip).limit(limit).all()

def edit_customer(id: str, customer_edit_input: Customer_edit_input, db:Session):
    db_user = db.query(Customer_model).get({"id":id})
    db_user.last_name = customer_edit_input.last_name
    db_user.first_name = customer_edit_input.first_name
    db_user.address = customer_edit_input.address
    db.commit()
    return db_user