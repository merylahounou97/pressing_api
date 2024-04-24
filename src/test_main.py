from fastapi.testclient import TestClient

from .main import app

from .sql.services.customer_service import Customer_service
from .sql.models.customer import Customer

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_customer():
    customer_service = Customer_service()
    
    customer = Customer(
        id= "",
        email="a@gmail.com",
        last_name="last",
        first_name="fist",
        address = "adhd"
    )
    
    