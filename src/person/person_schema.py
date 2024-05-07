from pydantic import BaseModel, ValidationError, constr, EmailStr, validator
import re

class Person(BaseModel):
    last_name: str
    first_name: str
    phone_number: constr(strip_whitespace=True, min_length=7, max_length=15)
    address: str
    email: EmailStr

    @validator('phone_number')
    def validate_phone_number(cls, v):
        if not re.match(r'^\+?\d{7,15}$', v):
            raise ValueError('Invalid phone number format')
        return v
