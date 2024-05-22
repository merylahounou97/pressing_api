from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import sessionmaker
from typing_extensions import Annotated

from src.customer import customer_service
from src.dependencies.db import get_db
from src.security import security_service


def check_token_validity(
    access_token: str, db: Annotated[sessionmaker, Depends(get_db)]
):
    """Check if the token is valid and if the user exists in the database.

    Args:
        access_token (str): The access token.
        db (Session): The database session.

    Raises:
        HTTPException: If the token is invalid or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security_service.decode_token(token=access_token)
        username: str = payload.get("sub")
        phone_number: str = payload.get("phone_number")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    user = customer_service.check_existing_customer(
        db=db, email=username, phone_number=phone_number
    )
    if user is None:
        raise credentials_exception
