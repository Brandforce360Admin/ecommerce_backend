import enum
import uuid

from sqlalchemy import Column, String, Enum, UUID, TIMESTAMP

from app.db.base import Base


class UserRole(enum.Enum):
    customer = "customer"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    _password_hash = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.customer)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=True)

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    @property
    def password_hash(self):
        """Getter for name attribute."""
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password_hash):
        self._password_hash = password_hash
