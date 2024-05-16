from typing_extensions import Annotated
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import BaseModel, Field, StringConstraints, EmailStr, field_validator 
import phonenumbers



class Phone_number(BaseModel):
    iso_code: str
    dial_code: str
    phone_text:  PhoneNumber

     # Ajout d'une méthode de validation personnalisée pour `phone_text`
    @field_validator('phone_text')
    def remove_tel_prefix(cls, v):
        return PhoneNumber.removeprefix(v,'tel:').replace("-","")


class Person_base_input(BaseModel):
    last_name: str
    first_name: str
    address: str
    email: EmailStr
    phone_number: Phone_number 

class Person(Person_base_input):
    phone_number_verified: bool  
    email_verified: bool  


class Person_verify_code_input(BaseModel):
    identifier: str
    verification_code: str

class Person_generate_new_validation_code_input(BaseModel):
    identifier: str
    strategy: str
    redirect_url: str

