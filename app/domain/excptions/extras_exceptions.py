class ExtraDoesNotExistsException(Exception):
    def __init__(self, message: str):
        self.message = message


class ExtraNotAvailableException(Exception):
    def __init__(self, message: str):
        self.message = message
