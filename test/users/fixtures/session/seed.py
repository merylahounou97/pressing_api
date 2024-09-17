
import pytest


customers = []
secretaries = []
admins = []

@pytest.fixture(scope="session")
def get_all_users():
    """Fixture pour récupérer tous les utilisateurs customers"""
    return customers

@pytest.fixture(scope="session")
def get_all_secretaries():
    return secretaries
    
@pytest.fixture(scope="session")
def get_all_admins():
    return admins