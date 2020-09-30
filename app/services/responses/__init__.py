"""
Common response and HTTP exceptions.
"""

from fastapi import HTTPException, status
from pydantic import BaseModel, Field


#######################################
#           Mixin Response            #
#######################################


class EmailMsg(BaseModel):
    """Email message schema"""

    detail: str = Field(example="Email sent")


class Msg(BaseModel):
    """Any detail operation mssage schema"""

    detail: str = Field(example="Opertion successfully")


#######################################
#           Error Responses           #
#######################################


class BadRequest_400(BaseModel):
    """Bad Request response schema"""

    detail: str = Field(example="Invalid request")


class Unauthorized_401(BaseModel):
    """Unauthorized response schema"""

    detail: str = Field(example="Invalid credential")


class Forbidden_403(BaseModel):
    """Forbidden response schema"""

    detail: str = Field(example="Operation forbidden")


class NotFound_404(BaseModel):
    """Not Found response schema"""

    detail: str = Field(example="Resource not found")


class Conflict_409(BaseModel):
    """Conflict response schema"""

    detail: str = Field(example="Operation forbidden")


class ServerError_500(BaseModel):
    """Server Error response schema"""

    detail: str = Field(example="Internal server error")


class _RaiseHTTPExceptions:
    """
    Helper class to handle the raising of exceptions.
    """

    def bad_request(self, detail: str) -> None:
        """Raise a 400 - BadRequest http exception"""
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail)

    def unauthorized(self) -> None:
        """Raise a 401 - Unauthorized http exception"""
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    def forbidden(self, detail: str) -> None:
        """Raise a 403 - Forbidden http exception"""
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail)

    def not_found(self, detail: str) -> None:
        """Raise a 404 - NotFound http exception"""
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail)

    def conflict(self, detail: str) -> None:
        """Raise a 409 - Conflict http exception"""
        raise HTTPException(status.HTTP_409_CONFLICT, detail)


raise_http_exception = _RaiseHTTPExceptions()
