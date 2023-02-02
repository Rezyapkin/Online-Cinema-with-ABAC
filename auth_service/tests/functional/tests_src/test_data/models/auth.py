from ipaddress import IPv6Address, IPv4Address

from pydantic import BaseModel

from tests_src.test_data.models.common import CommonRequest


class LogInRequest(BaseModel):
    email: str
    password: str
    ip: IPv4Address | IPv6Address
    user_agent: str


class ChangePasswordRequest(CommonRequest):
    new_password: str


class ChangeEmailRequest(CommonRequest):
    new_email: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: str
    token_type: str
