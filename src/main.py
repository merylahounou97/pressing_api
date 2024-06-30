from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.auth import auth_router
from src.config import Settings
from src.lifespans.create_default_admin import create_default_admin_lifespan
from .users import user_router
from .database import Base, engine

settings = Settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/",lifespan=create_default_admin_lifespan)

app.mount("/files", StaticFiles(directory="src/static/"), name="static")

app.include_router(user_router.router)
app.include_router(auth_router.router)
