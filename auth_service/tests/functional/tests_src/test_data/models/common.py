from ipaddress import IPv6Address, IPv4Address

from pydantic import BaseModel


class CommonRequest(BaseModel):
    token: str
    user_ip: IPv4Address | IPv6Address
    user_agent: str


class SuccessResponse(BaseModel):
    ...


class CommonPaginationResponse(BaseModel):
    total_count: int
    total_pages: int
    prev_page: int | None
    next_page: int | None


class ExpectedPagination(BaseModel):
    data_size: int
    prev_page: int | None
    next_page: int | None
