from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column

from src.person.person_model import PersonModel


class CustomerModel(PersonModel):
    """Modèle de client"""

    __tablename__ = "customers"
    id = mapped_column(ForeignKey("persons.id"), primary_key=True)
