from fastapi import APIRouter, HTTPException


from fastapi import Depends
from sqlalchemy.orm import Session

from src.database import SessionLocal, engine, Base
from src.config import Settings
from src.auth import auth_service
from src.auth.auth_schema import Login_input

settings = Settings()

router = APIRouter()



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Créer une route pour la connexion
@router.post("/login")
async def login(login: Login_input):
    db = SessionLocal()
    user = auth_service.authenticate_user(db, login.identifier, login.password)
    db.close()
    if user :
        user_data = {"email": user.email, 
                     "first_name": user.first_name, 
                     "last_name": user.last_name,
                     "phone_number": user.phone_number
                     }
        return user_data
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    


