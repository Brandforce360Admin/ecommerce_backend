import uuid


class SessionId:
    def __init__(self, session_id: uuid.UUID):
        self._session_id = session_id

    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        self._session_id = session_id
