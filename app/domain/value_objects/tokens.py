class AccessToken:
    def __init__(self, access_token: str):
        self._access_token = access_token

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, access_token):
        self._access_token = access_token


class RefreshToken:
    def __init__(self, refresh_token: str):
        self._refresh_token = refresh_token

    @property
    def refresh_token(self):
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, refresh_token):
        self._refresh_token = refresh_token


class Tokens:
    access_token: AccessToken
    refresh_token: RefreshToken

    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
