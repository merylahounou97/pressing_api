from typing_extensions import Annotated
from fastapi import APIRouter, HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


from src.config import Settings
from src.customer.customer_schema import Customer_create_output, Customer_create_input
from src.customer import customer_service
from src.dependencies.db import get_db

settings = Settings()

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")





@router.post("/customers", response_model=Customer_create_output)
def create_customers(customer: Customer_create_input , db: Session = Depends(get_db)):
    return customer_service.create_customer(db,customer) 

@router.get("/customers", response_model=list[Customer_create_output])
def read_users(access_token : Annotated[str,Depends(oauth2_scheme)],skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    users = customer_service.get_customers(db, skip=skip, limit=limit)
    return users
