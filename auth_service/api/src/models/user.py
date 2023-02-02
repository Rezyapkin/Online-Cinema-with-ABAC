from dataclasses import dataclass

from models.base import BasePagination
from models.common_request import CommonRequest, CommonPaginationRequest


@dataclass
class UserRequest(CommonRequest):
    id: str


@dataclass
class OAuthAccount:
    provider: str
    account_id: str


@dataclass
class UserResponse:
    id: str
    email: str
    is_active: bool
    is_superuser: bool
    oauth_accounts: list[OAuthAccount]


@dataclass
class UserMeResponse:
    email: str
    oauth_accounts: list[OAuthAccount]


@dataclass
class UserListRequest(CommonPaginationRequest):
    ...


@dataclass
class UserInList:
    id: str
    email: str
    is_active: bool
    is_superuser: bool


@dataclass
class UserListResponse:
    users: list[UserInList]
    pagination: BasePagination
