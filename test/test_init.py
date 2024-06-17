from fastapi.testclient import TestClient
from src.config import Settings
from src.database import Base, engine
from src.main import app

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

settings = Settings()

client = TestClient(app)
