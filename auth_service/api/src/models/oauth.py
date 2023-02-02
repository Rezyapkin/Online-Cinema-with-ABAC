from dataclasses import dataclass

from models.common_request import CommonRequest


@dataclass
class GetLoginUrlRequest:
    callback_url: str
    user_ip: str
    user_agent: str
    token: str | None


@dataclass
class GetLoginUrlResponse:
    url: str
    state: str


@dataclass
class OAuth2LogInRequest:
    code: str
    state: str
    user_ip: str
    user_agent: str


@dataclass
class OAuth2AttachAccountRequest(CommonRequest):
    code: str
    state: str
