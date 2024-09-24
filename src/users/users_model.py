import enum
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.types import Enum

from src.database import Base
from src.utils.constants import Constants


class UserRole(enum.Enum):
    """The role of the users"""

    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"
    SECRETARY = "SECRETARY"


class UserModel(Base):
    __tablename__ = Constants.USERS
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=True, default=None)
    phone_number = Column(String, unique=True, index=True, nullable=True, default=None)
    last_name = Column(String)
    first_name = Column(String)
    address = Column(String)
    password = Column(String)
    phone_number_verification_code = Column(String, default=None)
    phone_number_verification_expiry = Column(DateTime, default=None)
    email_verification_expiry = Column(DateTime, default=None)
    email_verification_code = Column(String, default=None)
    reset_password_code = Column(String, default=None)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    phone_number_verified = Column(
        Boolean, default=False
    )  # 0 pour non vérifié, 1 pour vérifié
    email_verified = Column(
        Boolean, default=False
    )  # 0 pour non vérifié, 1 pour vérifié

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
