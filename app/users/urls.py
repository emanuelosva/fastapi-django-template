"""
User router
"""

from fastapi import APIRouter, Body, Response, Depends, BackgroundTasks
from django.conf.global_settings import SESSION_COOKIE_AGE

from app.settings import DEBUG
from services import responses
from services.auth.utils import COOKIE_SESSION_NAME, create_access_token, get_auth_user
from services.email import send_welcome_email, send_recovery_password_email

from .views import userService
from .shcemas import UserDto, UserCreateDto, LoginUserDto, UserUpdateDto


#######################################
#            Users Router             #
#######################################

router = APIRouter()


#######################################
#         HTTP POST Operations        #
#######################################


@router.post(
    "/signup",
    status_code=201,
    response_model=UserDto,
    responses={
        "409": {"model": responses.Conflict_409},
    },
)
def create_a_new_user(
    user_info: UserCreateDto, response: Response, background_task: BackgroundTasks
) -> UserDto:
    """
    Signup: create a new user
    """
    user = userService.create_user(user_info)
    token = create_access_token(user.email)

    response.set_cookie(
        key=COOKIE_SESSION_NAME,
        value=token,
        max_age=SESSION_COOKIE_AGE,
        secure=not DEBUG,
        httponly=not DEBUG,
    )

    background_task.add_task(
        send_welcome_email,
        username=user.name,
        email=user.email,
    )
    return user


@router.post(
    "/login",
    response_model=UserDto,
    responses={
        "401": {"model": responses.Unauthorized_401},
    },
)
def login_a_user(credentials: LoginUserDto, response: Response) -> UserDto:
    """
    Login: Validate the user credentials and create a cookie session
    """
    user = userService.login_user(credentials)
    token = create_access_token(user.email)

    response.set_cookie(
        key=COOKIE_SESSION_NAME,
        value=token,
        max_age=SESSION_COOKIE_AGE,
        secure=not DEBUG,
        httponly=not DEBUG,
    )
    return user


@router.post(
    "/password-recovery/{email}",
    response_model=responses.EmailMsg,
    responses={"404": {"model": responses.NotFound_404}},
)
def sent_recovery_password_email(email: str, background_task: BackgroundTasks) -> any:
    """
    Verify is the email belogs to an active user and
    send a recovery password email.
    """
    token = userService.get_token_recovery_password(email)

    background_task.add_task(
        send_recovery_password_email,
        token=token,
        email=email,
    )
    return responses.EmailMsg(detail="Password recovery email sent")


@router.post(
    "/reset-password",
    response_model=responses.Msg,
    responses={"404": {"model": responses.NotFound_404}},
)
def reset_password(token: str = Body(...), new_password: str = Body(...)) -> any:
    """
    Verify is the email belogs to an active user and
    send a recovery password email.
    """
    userService.reset_password(token, new_password)
    # Only continues the execution if the token is valid
    # and the user is found and currently active
    return responses.Msg(detail="Password updated successfully")


#######################################
#         HTTP GET Operations         #
#######################################


@router.get(
    "/current",
    response_model=UserDto,
    responses={
        "401": {"model": responses.Unauthorized_401},
        "403": {"model": responses.Forbidden_403},
    },
)
def get_current_logged_user(user: UserDto = Depends(get_auth_user)) -> UserDto:
    """
    Extract the coockie session from request and retrieve the
    associated user if the cookie token is valid
    """
    return user


#######################################
#          HTTP PUT Operations        #
#######################################


@router.put(
    "/{user_id}",
    response_model=UserDto,
    responses={
        "401": {"model": responses.Unauthorized_401},
        "403": {"model": responses.Forbidden_403},
        "409": {"model": responses.Conflict_409},
    },
)
def update_user_info(
    user_id: int, user_info: UserUpdateDto, curret_user=Depends(get_auth_user)
) -> UserDto:
    """
    Update the user only if the session is active.
    """
    if curret_user.id != user_id:
        responses.raise_http_exception.forbidden("Forbidden")
    user = userService.update_user(user_id, user_info)
    return user
