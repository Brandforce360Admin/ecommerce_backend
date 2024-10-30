class UserName:
    def __init__(self, user_name: str):
        self._user_name = user_name

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        self._user_name = user_name
