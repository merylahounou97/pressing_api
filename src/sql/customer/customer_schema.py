
from src.sql.person.person_schema import Person


class Customer_create_output(Person):
    id: str


            
class Customer_create_input(Person):
    password: str