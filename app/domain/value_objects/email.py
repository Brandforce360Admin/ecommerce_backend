class Email:
    def __init__(self, email: str):
        self._email = email

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email
