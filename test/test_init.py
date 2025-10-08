from fastapi.testclient import TestClient
from src.config import get_settings, Settings
from src.main import app

settings = get_settings()

client = TestClient(app)
