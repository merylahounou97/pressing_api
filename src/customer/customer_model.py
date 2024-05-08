from src.person.person_model import Person_model
from sqlalchemy import  Column,  String,ForeignKey
from sqlalchemy.orm import mapped_column


class Customer_model(Person_model):
    __tablename__ = "customers"
    id = mapped_column(ForeignKey("persons.id"),primary_key=True)
