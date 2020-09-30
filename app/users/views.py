"""
View services layer for Users opearions.
"""

from django.db.utils import IntegrityError

from services.responses import raise_http_exception
from services.auth.utils import create_access_token, get_from_verify_token

from .models import User
from .shcemas import UserDto, UserCreateDto, LoginUserDto, UserUpdateDto


#######################################
#         User service Class          #
#######################################


class UsersViewsService:
    """
    Bussines Logic about users.
    """

    def create_user(self, user_info: UserCreateDto) -> UserDto:
        """
        Create a new user and return his/her info.

        Params:
        - user_info: USerCreateDto - The input user info.
        Returns:
        - user: UserDto - The created user
        """
        try:
            user = User(name=user_info.name, email=user_info.email)
            user.set_password(user_info.password)
            user.save()
        except IntegrityError:
            raise_http_exception.conflict("Email already exists")
        return UserDto.from_django(user)

    def login_user(self, credentials: LoginUserDto) -> UserDto:
        """
        Check user credentials and return the user info.

        Params:
        - credentials: LoginUserDto - The user credentials.
        Returns:
        - user: UserDto - The logged user
        """
        user = User.objects.filter(email=credentials.email).first()
        if not user or not user.check_password(credentials.password):
            raise_http_exception.unauthorized()
        return UserDto.from_django(user)

    def update_user(self, user_id: int, user_info: UserUpdateDto) -> UserDto:
        """
        Update the user info.

        Params:
        - user_id: str - The user ID for update
        - user_info: UserUpdateDto - The info for update
        Return:
        - user: UserDto - The user info after update
        """
        user = User.objects.get(id=user_id)
        if not user:
            raise_http_exception.not_found("User not found")
        if user_info.name:
            user.name = user_info.name
        if user_info.password:
            user.set_password(user_info.password)
        if user_info.email:
            user.email = user_info.email
        try:
            user.save()
        except IntegrityError:
            raise_http_exception.conflict("Email already exists")
        return user

    def get_token_recovery_password(self, email: str) -> str:
        """
        Verify if the email belongs to a current user and
        create a encoded token of short duration.

        Params:
        - email: str - The user email
        Return:
        - token: str - A short live encoded JWT
        """
        user = User.objects.filter(email=email).first()
        if not user:
            raise_http_exception.not_found("User not found")

        return create_access_token(user.email, recovery_password=True)

    def reset_password(self, token: str, new_password: str) -> None:
        """
        Verify the token and if it is valid update the user password.

        Params:
        - token: str - The token sent in recovery password email
        - new_password: str - The new user password
        Return:
        - None
        """
        email = get_from_verify_token(token)
        user = User.objects.filter(email=email).first()
        if not user:
            raise_http_exception.not_found("User not found")
        user.set_password(new_password)
        user.save()


#######################################
#       User service Instance         #
#######################################

# Allow to centrilize all methods abour user

userService = UsersViewsService()
