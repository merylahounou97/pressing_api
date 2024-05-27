from typing import Union

from src.person.person_schema import (Person,PersonInputBase, PersonVerificationInput)


class CustomerOutput(Person):
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


class CreateCustomerInput(PersonInputBase):
    """Create customer input model

    Attributes:
        password (str): The password of the customer
    """

    password: str


class CustomerEditInput(PersonInputBase):
    """Edit customer input model

    Attributes:
        password (str): The password of the customer
    """


class CustomerValidationCode(PersonVerificationInput):
    """Customer validation code model

    Attributes:
        identifier (str): The identifier of the customer
        verification_code (str): The verification code of the customer
    """


