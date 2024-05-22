from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class PhoneNumber(Base):
    """Phone number entity model.

    Attributes:
        phone_text (str): The phone number
        iso_code (str): The ISO code of the country
        dial_code (str): The dial code of the country
    """

    __tablename__ = "phone_numbers"
    phone_text = Column(String, primary_key=True)
    iso_code = Column(String)
    dial_code = Column(String)

    person: Mapped["PersonEntityModel"] = relationship(
        back_populates="phone_number", enable_typechecks=False
    )


class PersonEntityModel(Base):
    """Person entity model.

    Attributes:
        id (str): The unique identifier of the person
        email (str): The email of the person
        last_name (str): The last name of the person
        first_name (str): The first name of the person
        phone_number_id (str): The phone number of the person
        address (str): The address of the person
        password (str): The password of the person
        phone_number_verification_code (str): The verification code of the phone number
        phone_number_verification_expiry (datetime): The expiry date of the phone number verification code
        email_verification_expiry (datetime): The expiry date of the email verification code
        email_verification_code (str): The verification code of the email
        phone_number_verified (int): Indicates if the phone number is verified
        email_verified (int): Indicates if the email is verified
    """

    __tablename__ = "persons"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    last_name = Column(String)
    first_name = Column(String)
    phone_number_id = mapped_column(ForeignKey("phone_numbers.phone_text"))
    address = Column(String)
    password = Column(String)
    phone_number_verification_code = Column(String, default=None)
    phone_number_verification_expiry = Column(DateTime, default=None)
    email_verification_expiry = Column(DateTime, default=None)
    email_verification_code = Column(String, default=None)
    phone_number_verified = Column(
        Integer, default=0
    )  # 0 pour non vérifié, 1 pour vérifié
    email_verified = Column(Integer, default=0)  # 0 pour non vérifié, 1 pour vérifié
    phone_number: Mapped["PhoneNumber"] = relationship(back_populates="person")
