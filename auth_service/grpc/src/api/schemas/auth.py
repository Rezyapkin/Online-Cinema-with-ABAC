from pydantic import Field, validator
from email_validator import validate_email, EmailNotValidError

from models.base import BaseOrjsonModel


class LoginEntryDto(BaseOrjsonModel):
    login: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    user_agent: str
    ip_address: str


class LoginResulDto(BaseOrjsonModel):
    access_token: str
    refresh_token: str
    expires_in: int = Field(..., gt=0)
    token_type: str


class RefreshTokenEntryDto(BaseOrjsonModel):
    refresh_token: str = Field(..., min_length=1)
    user_agent: str


class RefreshTokenResultDto(BaseOrjsonModel):
    access_token: str
    refresh_token: str
    expires_in: int = Field(..., gt=0)
    token_type: str


class LogoutEntryDto(BaseOrjsonModel):
    access_token: str = Field(..., min_length=1)
    user_agent: str


class LogoutResultDto(BaseOrjsonModel):
    ...


class LogoutOtherEntryDto(BaseOrjsonModel):
    access_token: str = Field(..., min_length=1)
    user_agent: str


class LogoutOtherResultDto(BaseOrjsonModel):
    ...


class UpdatePasswordEntryDto(BaseOrjsonModel):
    access_token: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    user_agent: str


class UpdatePasswordResultDto(BaseOrjsonModel):
    ...


class UpdateEmailEntryDto(BaseOrjsonModel):
    access_token: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    user_agent: str

    @validator("email")
    def validate_email(cls, v):  # noqa: N805
        try:
            validate_email(v, check_deliverability=False)
        except EmailNotValidError:
            raise ValueError("not valid email")

        return v


class UpdateEmailResultDto(BaseOrjsonModel):
    ...


class CheckTokenEntryDto(BaseOrjsonModel):
    access_token: str = Field(..., min_length=1)
    user_agent: str


class CheckTokenResultDto(BaseOrjsonModel):
    success: bool
