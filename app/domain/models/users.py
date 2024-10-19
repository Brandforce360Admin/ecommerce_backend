import enum
import uuid

from sqlalchemy import Column, String, Enum, UUID, TIMESTAMP

from app.db.base import Base


class UserRole(enum.Enum):
    customer = "customer"
    admin = "admin"


class User(Base):
    __tablename__ = "users"
    # __table_args__ = {'schema': 'user_mgmt'}

    _user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    _name = Column(String(100), nullable=False)
    _email = Column(String(100), unique=True, nullable=False)
    _password_hash = Column(String(255), nullable=True)
    _role = Column(Enum(UserRole), default=UserRole.customer)
    _created_at = Column(TIMESTAMP, nullable=False)
    _updated_at = Column(TIMESTAMP, nullable=True)

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password_hash):
        self._password_hash = password_hash

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        self._created_at = created_at

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role):
        self._role = role
