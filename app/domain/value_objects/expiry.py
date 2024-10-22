from datetime import datetime


class Expiry:
    def __init__(self, expiry: datetime):
        self._expiry = expiry

    @property
    def expiry(self):
        return self._expiry

    @expiry.setter
    def expiry(self, expiry):
        self._expiry = expiry
