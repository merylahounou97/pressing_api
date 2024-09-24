import pytest
import unittest
from src.users.users_service import UserService


@pytest.mark.usefixtures("mock_users_service")
class TestUsersService(unittest.TestCase):
    pass
