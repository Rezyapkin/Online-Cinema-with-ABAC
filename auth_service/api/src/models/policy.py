from dataclasses import dataclass

from models.base import BasePagination
from models.common_request import CommonRequest, CommonPaginationRequest


@dataclass
class PolicyRequest(CommonRequest):
    id: str


@dataclass
class PolicyListRequest(CommonPaginationRequest):
    ...


@dataclass
class CreatePolicyRequest(CommonRequest):
    policy: dict


@dataclass
class CreatePolicyResponse:
    id: str


@dataclass
class UpdatePolicyRequest(CommonRequest):
    id: str
    policy: dict


@dataclass
class PolicyResponse:
    policy: dict


@dataclass
class PolicyListResponse:
    policies: list[dict]
    pagination: BasePagination
