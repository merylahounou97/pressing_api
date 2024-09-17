from src.users.users_schemas import UserCreateInput, UserCreateMemberInput
from src.users.users_service import UserService
import pytest

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