from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column

from src.person.person_model import Person_model


class Customer_model(Person_model):
    """The customer model"""

    __tablename__ = "customers"
    id = mapped_column(ForeignKey("persons.id"), primary_key=True)
