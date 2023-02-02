from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from models.postgres import Base
from models.postgres.base import UUIDMixin, TimeMixin


class UserRole(Base, UUIDMixin, TimeMixin):
    __tablename__ = "user_role"
    __mapper_args__ = {"eager_defaults": True}

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False)
