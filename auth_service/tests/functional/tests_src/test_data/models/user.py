from ipaddress import IPv6Address, IPv4Address
from datetime import datetime

from pydantic import BaseModel

from tests_src.test_data.models.common import CommonRequest, CommonPaginationResponse


class LogInHistoryRequest(CommonRequest):
    page_number: int
    page_size: int


class LogInHistory(BaseModel):
    date_time: datetime
    user_ip: IPv4Address | IPv6Address
    user_agent: str
    device: str


class LogInHistoryResponse(CommonPaginationResponse):
    data: list[LogInHistory]


class SignUpRequest(BaseModel):
    email: str
    password: str
    ip: IPv4Address | IPv6Address
    user_agent: str


class SignUpResponse(BaseModel):
    email: str
    id: str
