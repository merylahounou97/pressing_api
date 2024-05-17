# from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import sessionmaker
from typing_extensions import Annotated

from src.auth import auth_service
from src.auth.auth_schema import Login_input, Token
from src.config import Settings
from src.security.security_service import create_access_token

from ..dependencies.db import get_db

settings = Settings()

router = APIRouter()


# Créer une route pour la connexion
@router.post("/login")
async def login(login_input: Login_input, db: Annotated[sessionmaker, Depends(get_db)]):
    """Login a user

    args:
        login_input (Login_input): The login input
        db (Session): The database session

    Returns:
        dict: The user data
    """
    user = auth_service.authenticate_user(
        db, login_input.identifier, login_input.password
    )
    if user:
        user_data = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
        }
        return user_data
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/token")
def create_login_token(
    login_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[sessionmaker, Depends(get_db)],
):
    """Create a login token

    args:
        login_form (OAuth2PasswordRequestForm): The login form
        db (Session): The database session

    Returns:
        Token: The token
    """
    user = auth_service.authenticate_user(db, login_form.username, login_form.password)
    if user:
        access_token = create_access_token(
            data={"sub": user.email, "phone_number": user.phone_number_id}
        )
        return Token(access_token=access_token, token_type="Bearer")
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
