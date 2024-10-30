from fastapi import HTTPException, status


class InvalidTokenException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


class TokenExpiredException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


class UserAccessException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)


class UserNonLoggedInException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


class InvalidGoogleTokenException(Exception):
    def __init__(self, message: str):
        self.message = message
