from typing_extensions import Annotated
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import BaseModel, StringConstraints, EmailStr, field_validator 
import phonenumbers



class Phone_number(BaseModel):
    iso_code: str
    dial_code: str
    phone_text:  PhoneNumber

     # Ajout d'une méthode de validation personnalisée pour `phone_text`
    @field_validator('phone_text')
    def remove_tel_prefix(cls, v):
        return PhoneNumber.removeprefix(v,'tel:').replace("-","")

class Person(BaseModel):
    last_name: str
    first_name: str
    phone_number: Phone_number #Annotated[str, StringConstraints(strip_whitespace=True,min_length=7,max_length=15,pattern=r'^\+?\d{7,15}$')]  
    address: str
    email: EmailStr


