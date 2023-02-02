from uuid import UUID

from pydantic import BaseModel, Field


class UUIDMixin(BaseModel):
    uuid: UUID = Field(
        description="Уникальный идентификатор в формате UUID",
        example="524e4331-e14b-24d3-a456-426614174002",
    )
