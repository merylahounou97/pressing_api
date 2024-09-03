from src.users.users_model import UserRole
from test.test_init import client
from src.utils.constants import Constants
class BaseTestService:
    admins = []
    secretaries = []
    customers = []
    client= client
    def __init__(self, generate_user_data, create_user, get_access_token):
        self.secretaries = [generate_user_data(
            UserRole.SECRETARY) for i in range(2)]
        self.admins = [generate_user_data(UserRole.ADMIN) for i in range(2)]
        self.customers = [generate_user_data(
            UserRole.CUSTOMER) for i in range(2)]
        self.get_access_token = get_access_token
        self.generate_user_data = generate_user_data

        for admin in self.admins:
            create_user(admin, is_member=True)
        for secretary in self.secretaries:
            create_user(secretary, is_member=True)
        for customer in self.customers:
            create_user(customer)
