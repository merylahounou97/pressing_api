from typing_extensions import Annotated
from fastapi import Depends, HTTPException,status
from jose import JWTError
from src.customer import customer_service
from src.security import security_service
from src.dependencies.db import get_db
from sqlalchemy.orm import sessionmaker



def check_token_validity(access_token: str, db: Annotated[sessionmaker,Depends(get_db)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:  
        payload = security_service.decode_token(token=access_token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = customer_service.check_existing_customer(db=db,identifier=username  )
    if user is None:
        raise credentials_exception