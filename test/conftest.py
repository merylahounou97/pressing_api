from .base_fixtures import *
from test.users.fixtures.session import *

print("Global Imported catalog conftest")
from test.catalog.fixtures.session import *
