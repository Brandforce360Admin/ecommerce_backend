from app.domain.value_objects.session_id import SessionId
from app.domain.value_objects.user_id import UserId


class DecodedTokenDetails:
    def __init__(self, user_id, session_id, role):
        self.user_id: UserId = user_id
        self.session_id: SessionId = session_id
        self.role: str = role
