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
    person_id = Column(String, ForeignKey('persons.id'))
    person: Mapped["PersonModel"] = relationship(
        back_populates="phone_number", enable_typechecks=False,uselist=False,
    )


class PersonModel(Base):
    """Person entity model.

    Attributes:
        id (str): The unique identifier of the person
        email (str): The email of the person
        last_name (str): The last name of the person
        first_name (str): The first name of the person
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
    email = Column(String, unique=True, index=True, nullable=True, default=None)  
    last_name = Column(String)
    first_name = Column(String)
    address = Column(String)
    password = Column(String)
    phone_number_verification_code = Column(String, default=None)
    phone_number_verification_expiry = Column(DateTime, default=None)
    email_verification_expiry = Column(DateTime, default=None)
    email_verification_code = Column(String, default=None)
    reset_password_code = Column(String, default=None)
    phone_number_verified = Column(
        Integer, default=0
    )  # 0 pour non vérifié, 1 pour vérifié
    email_verified = Column(Integer, default=0)  # 0 pour non vérifié, 1 pour vérifié
    
    phone_number = relationship("PhoneNumber", back_populates="person",cascade="all", uselist=False,)

    def full_name(self):
        return self.first_name + " " + self.last_name

    def is_valid_email(self):
        """Check if the email is valid.
        Returns:
            bool: True if the email is valid, False otherwise
        """
        return self.email is not None and self.email_verified 
    
    def is_valid_phone_number(self):
        """Check if the phone number is valid.
        Returns:
            bool: True if the phone number is valid, False otherwise
        """
        return self.phone_number is not None and self.phone_number_verified
    
    def is_valid_one_identifier(self):
        """Check if the identifier is valid.
        Returns:
            bool: True if the identifier is valid, False otherwise
        """
        return self.is_valid_email() or self.is_valid_phone_number()