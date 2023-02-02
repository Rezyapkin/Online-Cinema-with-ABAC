import datetime
from uuid import UUID

from pydantic import Field, validator
from email_validator import validate_email, EmailNotValidError

from .base import BasePaginationEntryDto, BasePaginationResultDto
from models.base import BaseOrjsonModel


class CreateEntryDto(BaseOrjsonModel):
    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

    @validator("email")
    def validate_email(cls, v):  # noqa: N805
        try:
            validate_email(v, check_deliverability=False)
        except EmailNotValidError:
            raise ValueError("not valid email")

        return v


class CreateResultDto(BaseOrjsonModel):
    uuid: UUID
    email: str


class GetUserLoginHistoryEntryDto(BasePaginationEntryDto):
    access_token: str = Field(..., min_length=1)
    user_agent: str


class UserLoginHistory(BaseOrjsonModel):
    date: datetime.datetime | datetime.date
    device: str
    ip_address: str
    user_agent: str


class GetUserLoginHistoryResultDto(BasePaginationResultDto):
    results: list[UserLoginHistory]


class GetUserMeEntryDto(BaseOrjsonModel):
    access_token: str = Field(..., min_length=1)
    user_agent: str


class UserOAuthProviderAccountDto(BaseOrjsonModel):
    provider: str = Field(..., min_length=1)
    account_id: str = Field(..., min_length=1)


class GetUserMeResultDto(BaseOrjsonModel):
    email: str
    oauth_accounts: list[UserOAuthProviderAccountDto]
