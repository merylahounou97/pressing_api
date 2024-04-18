from fastapi.testclient import TestClient

from src.main import app,test_function

client = TestClient(app)


retour = test_function(a=1,b=2)
assert retour==3