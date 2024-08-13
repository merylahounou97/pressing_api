from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from src.auth.auth_schema import Token
from src.config import Settings
from src.security.security_service import create_access_token
from src.users.users_service import UserService


settings = Settings()

router = APIRouter(tags=["auth"])


@router.post("/token", response_model=Token)
def create_login_token(
    login_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends()],
):
    """Create a login token

    args:
        login_form (OAuth2PasswordRequestForm): The login form
        db (Session): The database session

    Returns:
        Token: The token
    """
    user = user_service.authenticate_user(login_form.username, login_form.password)

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
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

