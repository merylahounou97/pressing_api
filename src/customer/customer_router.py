from typing_extensions import Annotated
from fastapi import APIRouter, HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..security import security_service


from src.config import Settings
from src.customer.customer_schema import Customer_edit_input, Customer_output, Customer_create_input
from src.customer import customer_service
from src.dependencies.db import get_db

settings = Settings()

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



access_token_dep = Annotated[str,Depends(oauth2_scheme)]

@router.post("/customers", response_model=Customer_output)
async def  create_customers(customer: Customer_create_input , db: Session = Depends(get_db)):
    return await customer_service.create_customer(db,customer) 

@router.get("/customers", response_model=list[Customer_output])
def read_users(access_token : access_token_dep,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user = customer_service.validate_token(access_token=access_token,db=db)
    print(user)
    users = customer_service.get_customers(db=db, skip=skip, limit=limit)
    return users

@router.patch("/customers",response_model=Customer_output)
def edit_customer(customer_edit_input: Customer_edit_input,access_token : access_token_dep,db: Session = Depends(get_db) ):
    user = customer_service.validate_token(access_token=access_token,db=db)
    return customer_service.edit_customer(id=user.id, customer_edit_input= customer_edit_input,db=db)

