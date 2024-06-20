from src.person.person_schema import IdentifierEnum

from ..test_init import client

class TestCustomerRouter:
    def test_create_customer(self, mock_customer):
        data = mock_customer(IdentifierEnum.EMAIL)
        response = client.post(
            "/customers?redirect_url=google.com", json=data
        )
        response_payload = response.json()
        # Create user with phone number
        assert (
            response.status_code == 200
        ), "User with phone number created successfully"
        assert response_payload["email_verified"] is False
        assert response_payload["email"] is not None

        data = mock_customer(IdentifierEnum.PHONE_NUMBER)
        response = client.post(
            "/customers?redirect_url=google.com", json=data
        )
        response_payload = response.json()
        assert response.status_code == 200, "User with email created successfully"
        assert response_payload["phone_number_verified"] is False
        assert response_payload["phone_number"] is not None


        response = client.post(
            "/customers?redirect_url=google.com", json=mock_customer()
        )
        response_payload = response.json()
        assert response.status_code == 200, "user with both email and phone number not created"
        assert response_payload["phone_number_verified"] is False
        assert response_payload["phone_number"] is not None
        assert response_payload["email_verified"] is False
        assert response_payload["email"] is not None


    def test_verify_verification_code(
        self,get_customer_by_identifier_fix , mock_customer
    ):
        identifier =mock_customer()["email"]
        user_created = get_customer_by_identifier_fix(identifier)
        response = client.post(
            "/customers/verify_verification_code",
            json={
                "identifier": user_created.email,
                "verification_code": user_created.email_verification_code,
            },
        )
        response_payload = response.json()
        assert response.status_code == 200, "Verification code verified failed"
        assert response_payload["email_verified"] == True

        identifier =mock_customer()["phone_number"]

        user_created = get_customer_by_identifier_fix(identifier)
        response = client.post(
            "/customers/verify_verification_code",
            json={
                "identifier": user_created.phone_number,
                "verification_code": user_created.phone_number_verification_code,
            },
        )
        response_payload = response.json()
        assert response.status_code == 200, "Verification code verified failed"
        assert response_payload["phone_number_verified"] is True



    def test_edit_customer(self, get_access_token,mock_customer_with_both):       
        access_token = get_access_token(mock_customer_with_both["email"])
        edit_input = {
            "first_name": "first_name modified",
            "last_name": "last_name modified",
            "address": "address modified",
            "email": "ahounoumeryl@yahoo.fr",
            "phone_number": "+33751569562",
            "email_redirect_url": "http://localhost",
        }

        response = client.patch(
            "/customers",
            json=edit_input,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        response_payload = response.json()
        assert response.status_code == 200, "modification failed"
        assert "id" in response_payload
        assert response_payload["first_name"] == edit_input["first_name"]
        assert response_payload["last_name"] == edit_input["last_name"]
        assert response_payload["address"] == edit_input["address"]
        assert response_payload["email"] == edit_input["email"]
        assert response_payload["phone_number"] == edit_input["phone_number"]
        assert response_payload["email_verified"] is False
        assert response_payload["phone_number_verified"] is False
                

    def test_send_verification_code(self,get_customer_by_identifier_fix,
                                    mock_customer):
        #For email address
        idenfifier = mock_customer(IdentifierEnum.EMAIL)["email"]
        user = get_customer_by_identifier_fix(idenfifier)
        
        old_code = user.email_verification_code
        response =  client.post("/customers/send_verification_code", json={
            "identifier": idenfifier
        })
        assert response.status_code == 200, "Failed to send email verification"

        user = get_customer_by_identifier_fix(idenfifier)


        assert old_code != user.email_verification_code , "Code are the same"
        assert user.email_verified ==0, "Email verification should be false"

        #For phone number
        idenfifier =  mock_customer(IdentifierEnum.PHONE_NUMBER)["phone_number"]
        user = get_customer_by_identifier_fix(idenfifier)
        old_code = user.phone_number_verification_code

        response = client.post("/customers/send_verification_code", json={
            "identifier": idenfifier
        })

        assert response.status_code == 200, "Failed to send phone number verification"

        user = get_customer_by_identifier_fix(idenfifier)
        assert old_code != user.phone_number_verification_code , "Code are the same"
        assert user.phone_number_verified == 0, "Phone number verification should be false"


        
"""
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
