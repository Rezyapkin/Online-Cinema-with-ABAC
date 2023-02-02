from sqlalchemy import Column, String, Boolean

from models.postgres import Base, SchemaInDb
from models.postgres.base import UUIDMixin, TimeMixin


class User(Base, UUIDMixin, TimeMixin):
    __tablename__ = "user"
    __mapper_args__ = {"eager_defaults": True}

    email = Column(String(320), nullable=False, unique=True, index=True)
    hashed_password = Column(String(1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)


class UserSchema(SchemaInDb):
    email: str
    hashed_password: str
    is_active: bool | None
    is_superuser: bool | None
    is_verified: bool | None
