
import pytest
from test.users.users_test_service import UserTestService


@pytest.fixture
def user_test_service(generate_user_data , 
                       get_user_by_identifier, 
                       get_all_users, get_access_token,get_all_admins,get_all_secretaries):
    return UserTestService(generate_user_data,  
                            get_user_by_identifier, get_all_users, get_access_token,get_all_admins,get_all_secretaries)
