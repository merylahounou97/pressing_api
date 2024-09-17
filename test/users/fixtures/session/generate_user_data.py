from datetime import datetime, timedelta
import uuid
from passlib.hash import bcrypt
import pytest

from faker import Faker
from src.users.users_model import UserRole

fake = Faker()

@pytest.fixture(scope="session")
def generate_user_data():
    def _generate_user_data(role: UserRole = None, 
                            with_email=True,
                            with_phone_number=True, email_verified=False, 
                            phone_number_verified=False,email=None,phone_number=None):
        return {
            "id": str(uuid.uuid4()),
            "email":  fake.unique.email() if with_email and email is None else email,
            "phone_number":  f"+22997{fake.random_number(digits=6, fix_len=True)}" if with_phone_number and phone_number is None else phone_number,
            "last_name": fake.last_name(),
            "first_name": fake.first_name(),
            "address": fake.address(),
            "password": bcrypt.hash("string"),
            "phone_number_verification_code": str(fake.random_number(digits=6)),
            "phone_number_verification_expiry": str(datetime.now() + timedelta(days=1)),
            "email_verification_expiry": str(datetime.now() + timedelta(days=1)),
            "email_verification_code": str(fake.random_number(digits=6)),
            "reset_password_code": str(fake.random_number(digits=6)),
            "role":  role.value if role else fake.random_element(elements=[role.value for role in UserRole]),
            "phone_number_verified": phone_number_verified,
            "email_verified": email_verified

        }
    return _generate_user_data
