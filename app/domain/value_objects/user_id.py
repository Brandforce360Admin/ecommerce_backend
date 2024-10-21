import uuid

class UserId:
    def __init__(self, user_id: uuid.UUID):
        self._user_id = user_id

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id
