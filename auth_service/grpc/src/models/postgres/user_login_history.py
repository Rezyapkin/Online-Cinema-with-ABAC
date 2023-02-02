import uuid
from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, func, String, Boolean
from sqlalchemy.dialects.postgresql import UUID, ENUM

from models.postgres import Base, SchemaInDb
from models.postgres.base import UUIDMixin, CreatedTimeMixin


class DeviceEnum(str, Enum):
    web: str = "web"
    mobile: str = "mobile"
    smart_tv: str = "smart_tv"


class UserLoginHistory(Base, UUIDMixin, CreatedTimeMixin):
    __tablename__ = "user_login_history"
    __mapper_args__ = {"eager_defaults": True}
    __table_args__ = (
        {
            "postgresql_partition_by": "RANGE (created_at)",
        },
    )

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False)
    ip_address = Column(String(30))
    user_agent = Column(String(256))
    device = Column(ENUM(DeviceEnum), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)


class UserLoginHistorySchema(SchemaInDb):
    user_id: uuid.UUID
    user_agent: str | None
    ip_address: str
    device: str | DeviceEnum | None
    is_active: bool
