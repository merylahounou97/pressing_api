from src.person.person_schema import (
    PersonBaseSchemaCreate,
    PersonSchema,
    PersonBaseSchema,
)


class CustomerOutput(PersonSchema):
    """Customer output model

    Attributes:
        id (int): The customer id
        first_name (str): The first name of the customer
        last_name (str): The last name of the customer
        email (str): The email of the customer
        phone_number (str): The phone number of the customer
        address (str): The address of the customer
        is_active (bool): The status of the customer
        is_verified (bool): The verification status of the customer
    """

    id: str


class CreateCustomerInput(PersonBaseSchemaCreate):
    """Create customer input model

    Attributes:
        password (str): The password of the customer
    """

    password: str
