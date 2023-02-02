import orjson
from typing import Any
from uuid import UUID

from pydantic import Field, validator

from .base import BasePaginationEntryDto, BasePaginationResultDto
from models.base import BaseOrjsonModel


class GetUserEntryDto(BaseOrjsonModel):
    access_token: str = Field(..., min_length=1)
    id: UUID  # len is checked in validator
    user_agent: str


class AnyUserOAuthProviderAccountDto(BaseOrjsonModel):
    provider: str = Field(..., min_length=1)
    account_id: str = Field(..., min_length=1)


class GetUserResultDto(BaseOrjsonModel):
    id: UUID
    email: str
    is_active: bool
    is_superuser: bool
    oauth_accounts: list[AnyUserOAuthProviderAccountDto]


class GetUserListEntryDto(BasePaginationEntryDto):
    access_token: str = Field(..., min_length=1)
    user_agent: str

    # TODO: fixme


class UserInList(BaseOrjsonModel):
    id: UUID
    email: str
    is_active: bool
    is_superuser: bool


class GetUserListResultDto(BasePaginationResultDto):
    results: list[UserInList]


class CreatePolicyEntryDto(BaseOrjsonModel):
    access_token: str = Field(..., min_length=1)
    policy: str | dict[str, Any]
    user_agent: str

    @validator("policy")
    def policy_to_dict(cls, v):  # noqa: N805
        if isinstance(v, str):
            v = orjson.loads(v)

        return v


class CreatePolicyResultDto(BaseOrjsonModel):
    id: UUID


class UpdatePolicyEntryDto(BaseOrjsonModel):
    access_token: str = Field(..., min_length=1)
    id: UUID  # len is checked in validator
    policy: str | dict[str, Any]
    user_agent: str

    @validator("policy")
    def policy_to_dict(cls, v):  # noqa: N805
        if isinstance(v, str):
            v = orjson.loads(v)

        return v


class UpdatePolicyResultDto(BaseOrjsonModel):
    ...


class DeletePolicyEntryDto(BaseOrjsonModel):
    access_token: str = Field(..., min_length=1)
    id: UUID  # len is checked in validator
    user_agent: str


class DeletePolicyResultDto(BaseOrjsonModel):
    ...


class GetPolicyEntryDto(BaseOrjsonModel):
    access_token: str = Field(..., min_length=1)
    id: UUID  # len is checked in validator
    user_agent: str


class GetPolicyResultDto(BaseOrjsonModel):
    policy: str


class GetPolicyListEntryDto(BasePaginationEntryDto):
    access_token: str = Field(..., min_length=1)
    user_agent: str


class GetPolicyListResultDto(BasePaginationResultDto):
    policy: list[str]


class CheckAccessEntryDto(BaseOrjsonModel):
    access_token: str  # can be empty !
    inquiry: str | dict[str, Any]
    user_agent: str
    ip: str

    @validator("inquiry")
    def inquiry_to_dict(cls, v):  # noqa: N805
        if isinstance(v, str):
            v = orjson.loads(v)

        return v


class CheckAccessResultDto(BaseOrjsonModel):
    has_access: bool
