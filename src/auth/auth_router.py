from datetime import timedelta
from fastapi import APIRouter, HTTPException


from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.config import Settings
from src.auth import auth_service
from src.auth.auth_schema import Login_input, Token
from src.security.security_service import create_access_token
from ..dependencies.db import get_db
from typing_extensions import Annotated
from sqlalchemy.orm import sessionmaker



settings = Settings()

router = APIRouter()





# Créer une route pour la connexion
@router.post("/login")
async def login(login: Login_input,db: Annotated[sessionmaker,Depends(get_db)] ):
    user = auth_service.authenticate_user(db, login.identifier, login.password)
    if user :
        user_data = {"email": user.email, 
                     "first_name": user.first_name, 
                     "last_name": user.last_name,
                     "phone_number": user.phone_number
                     }
        return user_data
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/token")
def create_login_token(login:  Annotated[OAuth2PasswordRequestForm,Depends()],db: Annotated[sessionmaker,Depends(get_db)]):
    user = auth_service.authenticate_user(db, login.username, login.password)
    if user:
        access_token = create_access_token(
            data={"sub": user.email, 
                     "first_name": user.first_name, 
                     "last_name": user.last_name,
                     "phone_number": user.phone_number
                     }
        )
        return Token(access_token=access_token,token_type="Bearer")
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


    
