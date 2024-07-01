from fastapi.testclient import TestClient
from src.config import Settings
from src.main import app

settings = Settings()

client = TestClient(app)
