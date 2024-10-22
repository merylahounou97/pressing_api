from contextlib import asynccontextmanager
from logging import Logger

from fastapi import FastAPI

from src.lifespans.load_default_catalog import load_default_catalog_fun
from src.users.users_service import UserService
from src.database import SessionLocal
from src.auth.auth_router import settings



@asynccontextmanager
# Giving the app as an argument to the function is mandatory to have the lifespan working
async def initialize_app(app: FastAPI):
    """This function is used to initialize the app
    
    it creates the default admin user and loads the default catalog"""
    db = SessionLocal()

    user_service = UserService(db)
    
    await user_service.create_default_admin_user()
    
    load_default_catalog_fun(db)


    yield
    db.close()
