from fastapi import APIRouter


from fastapi import Depends
from sqlalchemy.orm import Session

from src.sql.database import SessionLocal, engine, Base
from src.config import Settings
from src.sql.customer.customer_schema import Customer_schema, Customer_create_schema
from src.sql.customer import customer_service

settings = Settings()

Base.metadata.create_all(bind=engine)

router = APIRouter()




# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/customers", response_model=Customer_schema)
def create_customers(customer: Customer_create_schema , db: Session = Depends(get_db)):
    return customer_service.create_customer(db,customer) 

@router.get("/customers", response_model=list[Customer_schema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = customer_service.get_customers(db, skip=skip, limit=limit)
    return users
