from unittest.mock import MagicMock
import pytest
from src.database import SessionLocal
from src.users.users_model import UserModel, UserRole
from src.users.users_schemas import UserCreateInput, UserCreateMemberInput
from src.database import Base, engine
from src.users.users_service import UserService
from test.users.conftest import generate_user_data, get_access_token


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


@pytest.fixture(scope="session")
def mock_db_session():
    """Fixture pour simuler une session de base de données"""
    return MagicMock()


@pytest.fixture(scope="session")
def get_test_db_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



@pytest.fixture(scope="session",autouse=True)
def setup_and_teardown(generate_user_data):
    """Fixture pour configurer et détruire la base de données"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    #Insérer des utilisateurs dans la base de donnéee
    _customers = [generate_user_data(role=UserRole.CUSTOMER) for _ in range(2)]
    _secretaries = [generate_user_data(role=UserRole.SECRETARY) for _ in range(2)]
    _admins = [generate_user_data(role=UserRole.ADMIN) for _ in range(2)]
    users = _customers + _secretaries + _admins
    with SessionLocal() as db:
        for user in users:
            db.add(UserModel(**user))
        db.commit()
    customers.extend(_customers)
    secretaries.extend(_secretaries)
    admins.extend(_admins)
    


@pytest.fixture
def create_user(get_test_db_session):
    """
    Create users in the test database
    user_data: dict The user data
    """
    def _create_user(user_data,is_member=False):
        if is_member:
            user = UserService(get_test_db_session).create(user_create_input=UserCreateMemberInput(**user_data))
        else:
            user = UserService(get_test_db_session).create(user_create_input=UserCreateInput(**user_data))
        return user
    return _create_user


