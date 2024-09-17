import pytest
from test.test_init import client

@pytest.fixture
def get_access_token():
    """Fixture pour récupérer un token d'accès"""

    def _access_token(
        identifier,
        password,
    ):
        response = client.post(
            "/token",
            data={"username": identifier, "password": password},
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
        )
        response_payload = response.json()
        return response_payload["access_token"]
    return _access_token