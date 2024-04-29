
from sqlalchemy.orm import Session
from .customer_model import Customer_model
from .customer_schema import Customer_schema, Customer_create_schema
import uuid

def create_customer(db: Session, customerCreate: Customer_create_schema):
    db_user = Customer_model(
        id= str(uuid.uuid4()),
        email =customerCreate.email,
        last_name =customerCreate.last_name,
        first_name =customerCreate.first_name,
        phone_number =customerCreate.phone_number,
        address =customerCreate.address,
        password =customerCreate.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer_model).offset(skip).limit(limit).all()
