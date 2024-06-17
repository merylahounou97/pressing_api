
from test.auth.test_auth_router import TestAuthRouter

import jose
import pytest
import sqlalchemy
import sqlalchemy.orm
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.customer.customer_model import CustomerModel
from src.dependencies.db import get_db
from src.sms.templates.messages import password_changed
from test.conftest import get_test_db_session

from ..test_init import client
from .mock_customer import (mock_change_password_input,
                            mock_customer_with_email,
                            mock_customer_with_phone_number,
                            mock_edit_customer,
                            mock_reset_and_validation_input,
                            mock_submit_reset_password_input,
                            mock_verify_identifier_input)


class TestCustomerRouter():

    access_token: str

    def test_create_customer(self,mock_customer_with_email,
                            mock_customer_with_phone_number):
        response = client.post("/customers?redirect_url=google.com", json=mock_customer_with_email);
        response_payload = response.json()

        print("response_payload +********************************", response_payload)
        
        #Create user with phone number
        assert response.status_code == 200, "User with phone number created successfully"
        assert response_payload["email_verified"] == False
        assert response_payload["email"] is not None 

        response = client.post("/customers?redirect_url=google.com", json=mock_customer_with_phone_number)
        response_payload = response.json()
        assert response.status_code == 200, "User with email created successfully"
        assert response_payload["phone_number_verified"] == False
        assert response_payload["phone_number"] is not None 


    def test_edit_customer(self,access_token):
        response = client.patch("/customers", json={
            "first_name": "first_name modified",
            "last_name": "last_name modified",
            "email_redirect_url": "http://localhost",
        }, headers={"Authorization": f"Bearer {access_token}"})
        response_payload = response.json()
        assert response.status_code == 200, "User with phone number edited successfully"
        assert "id" in response_payload
        assert response_payload["first_name"] == "first_name modified"
        assert response_payload["last_name"] == "last_name modified"

    def test_verify_verification_code(self,get_test_db_session,mock_customer_with_email):
        user_created = get_test_db_session.query(CustomerModel).filter(CustomerModel.email==mock_customer_with_email["email"]).first()
        response = client.post("/customers/verify_verification_code", json={
        "identifier": user_created.email ,
        "verification_code": user_created.email_verification_code}
        )
        response_payload = response.json()
        assert response.status_code == 200, "Verification code verified failed"
        assert response_payload["email_verified"] == True

"""
    def test_generate_new_email_validation_code(self):
        response = client.post("/customers/send_verification_code", json=mock_reset_and_validation_input)
        response_payload = response.json()
        
        assert response.status_code == 200, "New validation code generated successfully"
        assert response_payload["code_sent"] == True

    def test_change_password(self):
        user_online = "mock_user_online"  # Mock a valid user online
        response = client.patch(
            "/customers/change_password",
            json=mock_change_password_input,
            headers={"Authorization": f"Bearer {user_online}"}
        )
        response_payload = response.json()
        
        assert response.status_code == 200, "Password changed successfully"
        assert response_payload["password_changed"] == True

    def test_reset_password(self):
        identifier = "mock_identifier"  # Mock a valid identifier
        response = client.patch(f"/customers/reset_password?identifier={identifier}")
        response_payload = response.json()
        
        assert response.status_code == 200, "Password reset successfully"
        assert response_payload["reset"] == True

    def test_submit_reset_password(self):
        response = client.patch("/customers/submit_reset_password", json=mock_submit_reset_password_input)
        response_payload = response.json()
        
        assert response.status_code == 200, "Password submitted successfully"
        assert response_payload["password_reset"] == True"""