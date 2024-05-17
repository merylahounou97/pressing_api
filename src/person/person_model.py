from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Phone_number_model(Base):
    __tablename__ = "phone_numbers"
    phone_text = Column(String, primary_key=True)
    iso_code = Column(String)
    dial_code = Column(String)

    person: Mapped["Person_model"] = relationship(
        back_populates="phone_number", enable_typechecks=False
    )


class Person_model(Base):
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
    phone_number: Mapped["Phone_number_model"] = relationship(back_populates="person")
