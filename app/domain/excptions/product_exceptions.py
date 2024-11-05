class ProductDoesNotExistsException(Exception):
    def __init__(self, message: str):
        self.message = message


class ProductNotAvailableException(Exception):
    def __init__(self, message: str):
        self.message = message
