"""
Auth and security helpers
"""

from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security.api_key import APIKeyCookie
from jose import jwt, JWTError

from app.settings import SECRET_KEY
from services.responses import raise_http_exception
from users.shcemas import User, UserDto


#######################################
#       Auth & Seciruty Constants     #
#######################################

COOKIE_SESSION_NAME = "oreo_session_key"
auth_schema = APIKeyCookie(name=COOKIE_SESSION_NAME)


#######################################
#       Auth & Seciruty Helpers       #
#######################################


def create_access_token(email: str, recovery_password: bool = False) -> str:
    """
    Create a encoded JWT.

    Params:
    - email: str - The user email
    - recovery_password: bool - Indicate if the must have a short expiration time
    Return:
    - token: str - A encoded JWT
    """
    to_encode = {"email": email}
    expire_time = timedelta(days=15)

    if recovery_password:
        expire_time = timedelta(minutes=45)

    expires_in = datetime.utcnow() + expire_time
    to_encode.update({"exp": expires_in})
    return jwt.encode(to_encode, SECRET_KEY)


def get_from_verify_token(token: str) -> str:
    """
    Verify a encoded token and return the email in payload if is valid

    Params:
    - token: str - The encoded JWT
    Returns:
    - email: str - The email withn the JWT payload
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload["email"]
    except (JWTError, KeyError):
        raise_http_exception.unauthorized()
    return email


def get_auth_user(token: str = Depends(auth_schema)) -> UserDto:
    """
    Extract the token within the cookie session from the request
    object and verify it, then use the payload to find the user info

    Params:
    - token: str - The encode JWT in cookie request
    Rturn:
    - user: UserDto - The user info
    """
    email = get_from_verify_token(token)
    user = User.objects.filter(email=email).first()
    if not user:
        raise_http_exception.unauthorized()
    return UserDto.from_django(user)
