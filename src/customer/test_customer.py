
from ..test_init import client



mock_customer_with_phone = {
  "last_name": "Ahounou",
  "first_name": "Méryl",
  "address": "string",
  "phone_number": {
    "iso_code": "string",
    "dial_code": "string",
    "phone_text": "+33 6 66 49 52 44"
  },
  "password": "string"
}

mock_customer_with_email = {
  "last_name": "Aiounou",
  "first_name": "Ulrich",
  "address": "string",
  "email": "aiounouu@gmail.com",
  "password": "string"
}




def test_create_customer():
    response = client.post("/customers?redirect_url=google.com", json=mock_customer_with_phone);
    response_payload = response.json()
    #Create user with phone number
    assert response.status_code == 200
    assert response_payload["email_verified"] == False
    assert response_payload["phone_number_verified"] == False
    assert not (response_payload["email"] is None and response_payload["phone_number"]  is None)

    response = client.post("/customers?redirect_url=google.com", json=mock_customer_with_email);
    assert response.status_code == 200
