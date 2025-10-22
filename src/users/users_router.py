from typing import Optional, Union
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer

from src.config import get_settings
from src.users.users_service import UserService
from src.users.users_schemas import (
    ChangeUserPassword,
    ResetPasswordInput,
    UserBaseSchema,
    UserCreateInput,
    UserOutput,
    UserQueryOptions,
    VerifyIdentifierInput,
)
from src.users.users_model import UserModel, UserRole
from src.dependencies.get_user_online import GetUserOnline
from src.utils.constants import Constants
from src.utils.error_messages import ErrorMessages
from fastapi import APIRouter, Body, Depends, HTTPException, Query



router = APIRouter(prefix=f"/{Constants.USERS}", tags=[Constants.USERS])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


AccessTokenDep = Annotated[str, Depends(oauth2_scheme)]

UserServiceDep = Annotated[UserService, Depends()]


def get_user_online_dep(roles: list[UserRole] = None):
    return GetUserOnline(roles=roles)


@router.post("/", response_model=UserOutput)
def create_users(user: UserCreateInput, user_service: UserServiceDep):
    """Create a user with email or phone number

    Args:
        user (UserCreateInput): The user input

    Returns:
        UserOutput: The created user
    """
    return user_service.create(user_create_input=user)


@router.post("/verify_verification_code", response_model=UserOutput)
async def verify_verification_code(
    user_validation_code: VerifyIdentifierInput, user_service: UserServiceDep
):
    """Verify a verification code

    Args:
        verification (VerifyIdentifierInput): The verification code

    Returns:
        UserOutput: The verified user
    """
    return user_service.verify_code(verification=user_validation_code)


@router.post("/send_verification_code", response_model=Union[UserOutput, None])
def send_verification_code(
    identifier: Annotated[str, Body(embed=True)], user_service: UserServiceDep
):
    """Generate a validation code sent to the user by email or phone number

    Args:
        identifier: email or phone number

    Returns:
        bool: The result
    """
    return user_service.generate_new_validation_code(identifier=identifier)


@router.patch("/change_password", response_model=UserOutput)
def change_password(
    change_password_input: ChangeUserPassword,
    user_service: UserServiceDep,
    user_online: UserModel = Depends(get_user_online_dep()),
):
    """A router to Change a user password
    Args:
        change_password_input (Change_password_input): The change password input
        user_online (User_model, optional): The user online. Defaults to Depends(get_user_online).
        db (Session, optional): The database session. Defaults to Depends(get_db).

        Returns:
            User_output: The user output
    """
    return user_service.change_password(user_online, change_password_input)


@router.patch("/reset_password", response_model=UserOutput)
def reset_password(
    identifier: Annotated[str, Body(embed=True)], user_service: UserServiceDep
):
    """A router to reset a user password

    Args:

        identifier (str): The user identifier can be email or phone number
        db (Session, optional): The database session. Defaults to Depends(get_db).


        Returns:
            User_output: The user output"""
    identifier = identifier.replace(" ", "")

    return user_service.reset_password(identifier)


@router.patch("/submit_reset_password", response_model=UserOutput)
def submit_reset_password(
    reset_input: ResetPasswordInput, user_service: UserServiceDep
):
    """A router to submit a new password

    Args:

        reset_input (VerifyIdentifierInput): The reset input


        Returns:
            User_output: The user output"""
    return user_service.submit_reset_password(reset_input)


@router.patch("/", response_model=Union[UserOutput, None])
async def edit_user(
    user_edit_input: UserBaseSchema,
    user_service: UserServiceDep,
    user=Depends(get_user_online_dep()),
    user_id: Annotated[
        Optional[str],
        Query(
            description="The user id if the user online is a secretary or an admin",
            embed=False,
        ),
    ] = None,
):
    """Edit a user by id

    Args:
        user_edit_input (User_edit_input): The user edit input
        access_token (access_token_dep): The access token
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        User_output: The user output
    """

    if user.role == UserRole.ADMIN:
        # If the user is an admin or a secretary, they can edit any user
        if user_id is None:
            raise HTTPException(
                status_code=400, detail=ErrorMessages.USER_ID_NOT_PROVIDED
            )

        # Get the user to edit by id and edit it
        user_editing = user_service.get_user_by_id(user_id)

        if user_editing is None:
            raise HTTPException(status_code=404, detail=ErrorMessages.USER_NOT_FOUND)
        elif user_editing.role == UserRole.ADMIN:
            raise HTTPException(
                status_code=400, detail=ErrorMessages.ADMIN_CANNOT_EDIT_ADMIN
            )
        else:
            return user_service.edit_user(
                user_editing=user_editing, user_edit_input=user_edit_input
            )
    elif user.role == UserRole.SECRETARY:
        # If the user is a secretary, they can only edit a member
        if user_id is None:
            raise HTTPException(
                status_code=400, detail=ErrorMessages.USER_ID_NOT_PROVIDED
            )

        # Get the user to edit by id and edit it
        user_editing = user_service.get_user_by_id(user_id)

        if user_editing is None:
            raise HTTPException(status_code=404, detail=ErrorMessages.USER_NOT_FOUND)
        elif user_editing.role == UserRole.ADMIN:
            raise HTTPException(
                status_code=400, detail=ErrorMessages.SECRETARY_CANNOT_EDIT_ADMIN
            )
        elif user_editing.role == UserRole.SECRETARY:
            raise HTTPException(
                status_code=400, detail=ErrorMessages.SECRETARY_CANNOT_EDIT_SECRETARY
            )
        else:
            return user_service.edit_user(
                user_editing=user_editing, user_edit_input=user_edit_input
            )

    return user_service.edit_user(user_editing=user, user_edit_input=user_edit_input)


@router.get(
    "/",
    response_model=list[UserOutput],
    dependencies=[
        Depends(get_user_online_dep(roles=[UserRole.ADMIN, UserRole.SECRETARY]))
    ],
)
def get_all_users(
    user_service: UserServiceDep, user_query_options: UserQueryOptions = Depends(None)
):
    """Get all users
    Only an admin or a secretary can get all users
    Returns:
        List[UserOutput]: The list of users
    """
    return user_service.get_all_users(user_query_options)


@router.get("/me", response_model=UserOutput, tags=["me"])
def me(user=Depends(get_user_online_dep())):
    """Get the current user

    Returns:
        UserOutput: The current user
    """
    return user
