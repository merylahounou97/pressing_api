from sqlalchemy import  Column, String, ForeignKey, Integer
from sqlalchemy.orm import mapped_column,relationship,Mapped
from src.database import Base


class Phone_number_model(Base):
    __tablename__="phone_numbers"
    phone_text = Column(String,primary_key=True)
    iso_code= Column(String)
    dial_code=Column(String)

    person: Mapped["Person_model"] = relationship(
        back_populates="phone_number",enable_typechecks=False
    )

class Person_model(Base):
    __tablename__ = "persons"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    last_name = Column(String)
    first_name = Column(String)
    phone_number_id= mapped_column(ForeignKey("phone_numbers.phone_text"))
    address = Column(String)
    password = Column(String)
    verification_code = Column(String, index=True)
    is_verified = Column(Integer, default=0)  # 0 pour non vérifié, 1 pour vérifié
    
    phone_number: Mapped["Phone_number_model"] = relationship(
        back_populates="person"
    )
