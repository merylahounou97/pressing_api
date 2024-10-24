import pytest
from test.users.members_test_service import MembersTestService


@pytest.fixture
def member_test_service(
    generate_user_data,
    get_user_by_identifier,
    get_all_users,
    get_access_token,
    get_all_admins,
    get_all_secretaries,
):
    return MembersTestService(
        generate_user_data,
        get_user_by_identifier,
        get_all_users,
        get_access_token,
        get_all_admins,
        get_all_secretaries,
    )
