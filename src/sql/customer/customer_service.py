
from sqlalchemy.orm import Session
from .customer_model import Customer_model
from .customer_schema import Customer_schema, Customer_create_schema
import uuid
from passlib.hash import bcrypt
from fastapi import HTTPException



def check_existing_customer(db: Session, phone_number: str, email):
    user_by_phone_number = db.query(Customer_model).filter(Customer_model.phone_number == phone_number).first()
    user_by_email = db.query(Customer_model).filter(Customer_model.email == email).first()
    if user_by_phone_number and user_by_email:
        return True
    return False


def create_customer(db: Session, customerCreate: Customer_create_schema):
    if check_existing_customer(db, customerCreate.phone_number, customerCreate.email):
        raise HTTPException(status_code=400, detail="Phone number or email already registered")
    
    hashed_password = bcrypt.hash(customerCreate.password)
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