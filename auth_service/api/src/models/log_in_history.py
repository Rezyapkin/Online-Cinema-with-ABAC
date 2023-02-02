from dataclasses import dataclass
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address

from models.base import BasePagination
from models.common_request import CommonPaginationRequest


@dataclass
class LogInHistoryRequest(CommonPaginationRequest):
    ...


@dataclass
class LogInHistoryItem:
    date_time: datetime
    user_ip: IPv4Address | IPv6Address
    user_agent: str
    device: str


@dataclass
class LogInHistoryResponse:
    data: list[LogInHistoryItem]
    pagination: BasePagination
