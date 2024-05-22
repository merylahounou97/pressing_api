from typing import Union

from src.person.person_schema import (
    Person, Person_base_input, PersonGenerateNewvalidationCodeInput,
    Person_verify_code_input)


class CustomerOutput(Person):
    id: str
    phone_number_verification_code: Union[str, None]

    email_verification_code: Union[str, None]


class Customer_create_input(Person_base_input):
    password: str


class Customer_edit_input(Person_base_input):
    pass


class Customer_verify_code(Person_verify_code_input):
    pass


class Customer_generate_new_validation_code_input(
    PersonGenerateNewvalidationCodeInput
):
    pass
