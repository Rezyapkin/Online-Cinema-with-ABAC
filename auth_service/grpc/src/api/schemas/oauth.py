from pydantic import Field, HttpUrl
from models.base import BaseOrjsonModel


class GetProviderLoginURLEntryDto(BaseOrjsonModel):
    callback_url: HttpUrl
    access_token: str | None
    user_agent: str


class ProviderLoginURLResultDto(BaseOrjsonModel):
    url: HttpUrl
    state_token: str


class OAuthLoginEntryDto(BaseOrjsonModel):
    code: str = Field(..., min_length=1)
    state_token: str
    ip_address: str
    user_agent: str


class OAuthLoginResultDto(BaseOrjsonModel):
    access_token: str
    refresh_token: str
    expires_in: int = Field(..., gt=0)
    token_type: str


class AttachAccountToUserEntryDto(OAuthLoginEntryDto):
    access_token: str = Field(..., min_length=1)


class DetachAccountFromUserEntryDto(BaseOrjsonModel):
    access_token: str = Field(..., min_length=1)
    user_agent: str


class AttachAccountResultDto(BaseOrjsonModel):
    ...


class DetachAccountResultDto(BaseOrjsonModel):
    ...
