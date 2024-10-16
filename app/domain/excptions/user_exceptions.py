class UserAlreadyExistsException(Exception):
    def __init__(self, message: str):
        self.message = message


class InvalidPasswordException(Exception):
    def __init__(self, message: str):
        self.message = message
