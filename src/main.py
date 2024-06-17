from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.auth import auth_router
from src.config import Settings
from .customer import customer_router
from .database import Base, engine

settings = Settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/")

app.mount("/files", StaticFiles(directory="src/static/"), name="static")

app.include_router(customer_router.router)
app.include_router(auth_router.router)
