from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.domain.excptions.user_exceptions import UserAlreadyExistsException


def user_already_exists_exception_handler(request: Request, exc: UserAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": str(exc)},
    )
