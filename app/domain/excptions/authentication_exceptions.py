class InvalidTokenException(Exception):
    def __init__(self, message: str):
        self.message = message

class TokenExpiredException(Exception):
    def __init__(self, message: str):
        self.message = message


class UserAccessException(Exception):
    def __init__(self, message: str):
        self.message = message
