import json

import pytest
from fastapi.testclient import TestClient
from pytest_mock import mocker

from src.sql.customer.customer_model import Customer_model
from src.sql.customer.customer_schema import Customer_schema
from src.sql.customer.customer_service import create_customer

from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Ceci est un pressing de wash man"


@pytest.fixture
def mock_create_customer(mocker):
    return mocker.patch("src.sql.customer.customer_service.create_customer")


def test_create_customer():
    customer = Customer_schema(
        id="jychv",
        email="a@gmail.com",
        last_name="last",
        first_name="fist",
        address="adhd",
        password="password123",
        phone_number="+33745346489",
    )


@pytest.fixture
def mock_authenticate_user(mocker):
    return mocker.patch(
        "src.sql.login.login_service.authenticate_user",
        return_value={
            "id": "test_id",
            "email": "a@gmail.com",
            "last_name": "last",
            "first_name": "first",
            "address": "adhd",
            "password": "password123",
            "phone_number": "+33745346489",
        },
    )


# Test de la fonction de connexion avec des identifiants valides
def test_login_valid(mock_authenticate_user):

    # Envoyer une requête POST avec des identifiants valides
    response = client.post(
        "/login", json={"identifier": "a@gmail.com", "password": "password123"}
    )

    # Vérifier que le statut de la réponse est 200 OK
    assert response.status_code == 200

    # Envoyer une requête POST avec des identifiants valides
    response = client.post(
        "/login", json={"identifier": "+33745346489", "password": "password123"}
    )

    # Vérifier que le statut de la réponse est 200 OK
    assert response.status_code == 200

    # Vérifier que les données de l'utilisateur sont correctes dans la réponse
    assert response.json() == {
        "email": "a@gmail.com",
        "first_name": "first",
        "last_name": "last",
        "phone_number": "+33745346489",
    }
