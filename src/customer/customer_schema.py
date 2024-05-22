from typing import Union

from src.person.person_schema import (Person,
                                      PersonGenerateNewvalidationCodeInput,
                                      PersonInputBase, PersonVerificationInput)


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
    phone_number_verification_code: Union[str, None]

    email_verification_code: Union[str, None]


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


class CustomerNewValidationCodeInput(PersonGenerateNewvalidationCodeInput):
    """Customer new validation code input model

    Attributes:
        identifier (str): The identifier of the customer
    """