import uuid

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID


class UUIDMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class CreatedTimeMixin:
    created_at = Column(DateTime, default=func.now(), nullable=False)


class TimeMixin(CreatedTimeMixin):
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
