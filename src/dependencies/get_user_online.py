from fastapi import Depends, HTTPException
from src.dependencies.get_customer_online import get_user_online
from src.users.users_model import UserModel, UserRole


class GetUserOnline:
    """This is a dependency that  decode the access token of a user and return the instance of the user
    Args:
        access_token (str): The access token.
        db (Session): The database session.
        roles (list): The roles that have access to the resource, defaults to None
            let it to None if you want to allow all roles to access the resource.


    Returns:
        UserModel: The user instance.
    """
    def __init__(self,roles: list[UserRole] = None):
        self.roles = roles

    def __call__(self,user_online: UserModel =Depends(get_user_online) ):
        if self.roles and  user_online.role not in self.roles:
            raise HTTPException(
                status_code=401,
                detail="You do not have permission to access this resource",
            )
        return user_online