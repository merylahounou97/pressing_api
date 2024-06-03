from typing_extensions import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.orm import Session
from src.customer import customer_service
from src.dependencies.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

AccessTokenDep = Annotated[str, Depends(oauth2_scheme)]

def get_customer_online(access_token: AccessTokenDep, db: Session = Depends(get_db)):
    """Get the user online

    Args:
        access_token (access_token_dep): The access token
        db (Session, optional): The database session. Defaults to Depends(get_db).

        Returns:
            Customer_model: The user

            """
    return customer_service.validate_token(access_token=access_token, db=db)
