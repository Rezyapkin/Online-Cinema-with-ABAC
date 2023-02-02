from dataclasses import dataclass


@dataclass
class CommonRequest:
    token: str
    user_ip: str
    user_agent: str


@dataclass
class CommonPaginationRequest(CommonRequest):
    page_number: int
    page_size: int
