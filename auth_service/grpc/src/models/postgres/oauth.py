import uuid
from enum import Enum

from sqlalchemy import Column, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID, ENUM

from models.postgres import Base, SchemaInDb
from models.postgres.base import UUIDMixin, CreatedTimeMixin


class OAuthProviderEnum(str, Enum):
    google: str = "google"
    yandex: str = "yandex"


class UserOAuthAccount(Base, UUIDMixin, CreatedTimeMixin):
    __tablename__ = "user_oauth_account"
    __mapper_args__ = {"eager_defaults": True}

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    oauth_provider_name = Column(ENUM(OAuthProviderEnum), nullable=False)
    oauth_account_id = Column(String(60), nullable=False)

    __table_args__ = (
        Index("ix_provider_account", "oauth_provider_name", "oauth_account_id", unique=True),
        Index("ix_user_provider", "user_id", "oauth_provider_name", unique=True),
    )


class UserOAuthAccountSchema(SchemaInDb):
    user_id: uuid.UUID
    oauth_provider_name: str | OAuthProviderEnum
    oauth_account_id: str
