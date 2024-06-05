from fastapi.testclient import TestClient
import pytest
from src.config import Settings
from .database import Base, engine
from .main import app


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

settings = Settings()

client = TestClient(app)


