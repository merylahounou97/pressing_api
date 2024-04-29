from pydantic import BaseModel, EmailStr

class Customer_create_schema(BaseModel):
    email: EmailStr
    last_name: str
    first_name: str
    phone_number: str
    address: str
    password: str

class Customer_schema(Customer_create_schema):
    id: str