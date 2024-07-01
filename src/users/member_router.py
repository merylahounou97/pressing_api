from typing_extensions import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from src.config import Settings
from src.users.users_router import get_user_online_dep
from src.users.users_service import UserService
from src.users.users_schemas import (UserCreateMemberInput, UserOutput)
from src.users.users_model import UserRole
from src.utils.constants import Constants


settings = Settings()

router = APIRouter(prefix=f"/{Constants.MEMBER}",tags=[Constants.MEMBER])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


AccessTokenDep = Annotated[str, Depends(oauth2_scheme)]

UserServiceDep =Annotated[UserService, Depends()]


@router.post("/",
             summary="Create a secretary or an administrator",
             response_model=UserOutput ,
             dependencies=[Depends(get_user_online_dep([UserRole.ADMIN]))])
def create_secretary(
    member_input: UserCreateMemberInput, user_service: UserServiceDep):
    """Create a secretary or administrator

    Only an admin can create a secretary

    Args:
        user (UserCreateInput): The user input
    Returns:
        UserOutput: The created user
    """
    return user_service.create(user_create_input=member_input)
