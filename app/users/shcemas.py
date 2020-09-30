"""
User schemas - DataTransferObjects (DTO).
"""

from typing import Optional
from pydantic_django import PydanticDjangoModel
from pydantic import BaseModel, Field
from .models import User


#######################################
#             User Schema             #
#######################################


class UserDto(PydanticDjangoModel):
    """
    Pydantic User schema from User django model.
    """

    class Config:
        """Inherit properties from model"""

        model = User
        exclude = [
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "logentry",
            "date_joined",
            "groups",
            "user_permissions",
            "last_login",
        ]
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Tiangolo",
                "email": "tiangolo@email.com",
                "created_at": "2020-09-30T03:05:14.802506+00:00",
                "updated_at": "2020-09-30T03:05:14.802518+00:00",
            }
        }


#######################################
#         User Inputs Schemas         #
#######################################


class LoginUserDto(BaseModel):
    """
    Pydantic schema for login a user.
    """

    email: str = Field(..., example="tiangolo@email.com")
    password: str = Field(..., example="fastapi-and-django")


class UserCreateDto(LoginUserDto):
    """
    Pydantic User create input schema.
    """

    name: str = Field(..., example="Tiangolo")


class UserUpdateDto(BaseModel):
    """
    Pydantic User update input schema.
    """

    name: Optional[str] = Field(None, example="Guido V.R")
    email: Optional[str] = Field(None, example="guido@python.com")
    password: Optional[str] = Field(None, example="pythonico")
