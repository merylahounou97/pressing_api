
from sqlalchemy import or_
from sqlalchemy.orm import Session
from .customer_model import Customer_model
from .customer_schema import Customer_create_output, Customer_create_input
import uuid
from fastapi import HTTPException

from ..security import security_service 

def check_existing_customer(db: Session, identifier: str):
    user = get_customer_by_email_or_phone(db, identifier, identifier)
    return user is not None

def get_customer_by_email_or_phone(db: Session, email: str, phone_number: str):
    return db.query(Customer_model).filter( or_(Customer_model.phone_number == phone_number, Customer_model.email == email)  ).first()


def create_customer(db: Session, customerCreate: Customer_create_input):
    if check_existing_customer(db, customerCreate.phone_number, customerCreate.email):
        raise HTTPException(status_code=400, detail="Phone number or email already registered")
    
    hashed_password = security_service.hashText(customerCreate.password)
    db_user = Customer_model(
        id= str(uuid.uuid4()),
        email =customerCreate.email,
        last_name =customerCreate.last_name,
        first_name =customerCreate.first_name,
        phone_number =customerCreate.phone_number,
        address =customerCreate.address,
        password =hashed_password 
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer_model).offset(skip).limit(limit).all()