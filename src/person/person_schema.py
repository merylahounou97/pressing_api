from pydantic import BaseModel, EmailStr

class Person(BaseModel):
    last_name: str
    first_name: str
    phone_number: str
    address: str  
    email: EmailStr