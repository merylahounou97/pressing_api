import pytest
from sqlalchemy import or_

from src.users.users_model import UserModel


@pytest.fixture
def get_user_by_identifier(get_test_db_session):
    """
    Get a user by identifier in the test database
    identifier: str The identifier of the user
    """

    def _get_user_by_identifier(identifier: str) -> UserModel:
        return (
            get_test_db_session.query(UserModel)
            .filter(
                or_(
                    UserModel.phone_number == identifier,
                    UserModel.email == identifier,
                )
            )
            .populate_existing()
            .first()
        )

    return _get_user_by_identifier
