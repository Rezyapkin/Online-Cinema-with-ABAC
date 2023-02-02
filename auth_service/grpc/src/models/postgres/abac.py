import uuid
from typing import Any

from pydantic import validator, Field
from sqlalchemy import Column, ForeignKey, Text, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.postgres import Base, SchemaInDb
from models.postgres.base import UUIDMixin, TimeMixin
from services.abac.effects import Effects


class PolicySubjectModel(Base, UUIDMixin, TimeMixin):
    """Storage model for policy subjects"""

    __tablename__ = "policy_subjects"
    __mapper_args__ = {"eager_defaults": True}

    policy_id = Column(UUID(as_uuid=True), ForeignKey("policy.id", ondelete="CASCADE"), index=True, nullable=False)
    subject = Column(JSON(), comment="JSON value for rule-based policies")


class PolicySubjectModelSchema(SchemaInDb):
    policy_id: uuid.UUID
    subject: dict[str, Any]


class PolicyResourceModel(Base, UUIDMixin, TimeMixin):
    """Storage model for policy resources"""

    __tablename__ = "policy_resources"
    __mapper_args__ = {"eager_defaults": True}

    policy_id = Column(UUID(as_uuid=True), ForeignKey("policy.id", ondelete="CASCADE"), index=True, nullable=False)
    resource = Column(JSON(), comment="JSON value for rule-based policies")


class PolicyResourceModelSchema(SchemaInDb):
    policy_id: uuid.UUID
    resource: dict[str, Any]


class PolicyActionModel(Base, UUIDMixin, TimeMixin):
    """Storage model for policy actions"""

    __tablename__ = "policy_actions"
    __mapper_args__ = {"eager_defaults": True}

    policy_id = Column(UUID(as_uuid=True), ForeignKey("policy.id", ondelete="CASCADE"), index=True, nullable=False)
    action = Column(JSON(), comment="JSON value for rule-based policies")


class PolicyActionModelSchema(SchemaInDb):
    policy_id: uuid.UUID
    action: dict[str, Any]


class PolicyModel(Base, UUIDMixin, TimeMixin):
    """Storage model for policy"""

    __tablename__ = "policy"
    __mapper_args__ = {"eager_defaults": True}

    description = Column(Text(), unique=True, nullable=False)
    effect = Column(Boolean(), nullable=False)
    context = Column(JSON())
    subjects = relationship("PolicySubjectModel", passive_deletes="all", lazy="joined")
    resources = relationship("PolicyResourceModel", passive_deletes="all", lazy="joined")
    actions = relationship("PolicyActionModel", passive_deletes="all", lazy="joined")


class PolicyModelSchema(SchemaInDb):
    description: str
    effect: bool | Effects
    context: dict[str, Any] = Field(default_factory=dict)
    subjects: list[Any | dict[str, Any]] | None
    resources: list[Any | dict[str, Any]] | None
    actions: list[Any | dict[str, Any]] | None

    @validator("effect")
    def validate_effect(cls, v):  # noqa: N
        if isinstance(v, Effects):
            v = v == Effects.ALLOW_ACCESS

        return v
