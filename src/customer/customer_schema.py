
from src.person.person_schema import Person
from src.person.person_schema import Person_base


class Customer_output(Person):
    id: str


            
class Customer_create_input(Person):
    password: str


class Customer_edit_input(Person_base):
    pass