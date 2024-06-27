from typing_extensions import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from src.users.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

AccessTokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_user_online(access_token: AccessTokenDep, 
                    user_service: Annotated[UserService, Depends()]):
    """This is a dependency that  decode the access token of a user and return the instance of the user
    Args:
        access_token (str): The access token.
        db (Session): The database session.
        roles (list): The roles that have access to the resource, defaults to None
            let it to None if you want to allow all roles to access the resource.

    Raises:
        HTTPException: If the token is invalid or the user does not exist.
        or the user does not have the required role.

    Returns:
        UserModel: The user instance.
    """
    user= user_service.validate_token(access_token=access_token)
    return user
