from sqlalchemy import  Column,  String
# from pydantic import EmailStr

class Person_model:
    __tablename__ = "persons"
    id = Column(String, primary_key=True)
    email = Column(String(150), unique=True, index=True)
    last_name = Column(String(100))
    first_name = Column(String(100))
    phone_number = Column(String(50))
    address = Column(String(255))
    password = Column(String)
    
    # @staticmethod
    # def validate_email(email: str) -> EmailStr:
    #     return EmailStr(email)