import uuid
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, UUID, TIMESTAMP
from sqlalchemy.orm import relationship

from app.db.base import Base


class Session(Base):
    __tablename__ = "sessions"
    _session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    _user_id = Column(UUID(as_uuid=True), ForeignKey("users._user_id"), nullable=False)
    _refresh_token = Column(String, index=True, nullable=False)
    _expires_at = Column(TIMESTAMP, nullable=False)
    _user = relationship("User")

    def __init__(self, session_id: UUID, user_id: UUID, refresh_token: str, expires_at: datetime):
        self._session_id = session_id
        self._user_id = user_id
        self._refresh_token = refresh_token
        self._expires_at = expires_at
