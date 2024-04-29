from sqlalchemy import  Column,  String

class Person_model:
    __tablename__ = "persons"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    last_name = Column(String)
    first_name = Column(String)
    phone_number = Column(String)
    address = Column(String)
    password = Column(String)