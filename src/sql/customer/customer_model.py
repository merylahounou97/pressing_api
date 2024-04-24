from src.sql.person.person_model import Person_model
from src.sql.database import Base

class Customer_model(Person_model,Base):
    __tablename__ = "customers"
    pass
