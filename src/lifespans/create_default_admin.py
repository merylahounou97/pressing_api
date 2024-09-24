from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.users.users_service import UserService
from src.database import SessionLocal
from src.auth.auth_router import settings


@asynccontextmanager
# Giving the app as an argument to the function is mandatory to have the lifespan working
async def create_default_admin_lifespan(app: FastAPI):
    """Create the default admin user in the database"""
    db = SessionLocal()
    user_service = UserService(db)
    # await user_service.create_default_admin_user()
    yield
    db.close()
