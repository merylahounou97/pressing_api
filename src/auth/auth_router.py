from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import sessionmaker
from typing_extensions import Annotated

from src.customer import customer_service
from src.auth.auth_schema import LoginForm, Token
from src.config import Settings
from src.security.security_service import create_access_token

from ..dependencies.db import get_db

settings = Settings()

router = APIRouter()


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
    print(login_form.username, login_form.password)
    user = customer_service.authenticate_user(
        db, login_form.username, login_form.password
    )
    if user:
        access_token = create_access_token(
            data={
                "sub": user.id,
                "email": user.email,
                "phone_number": user.phone_number
                if user.phone_number is not None
                else None,
            }
        )
        return Token(access_token=access_token, token_type="Bearer")
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
