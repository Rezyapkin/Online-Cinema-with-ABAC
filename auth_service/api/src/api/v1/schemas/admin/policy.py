from dataclasses import dataclass

from flasgger import Schema, fields
from marshmallow import post_load

from api.v1.schemas.connect_info import ConnectionInfo
from api.v1.schemas.pagination import PaginationSchema, RequestWithPagination, PaginationResponseSchema
from models.policy import (
    PolicyListRequest as PolicyListModel,
    PolicyRequest as PolicyModel,
    CreatePolicyRequest as CreatePolicyModel,
    UpdatePolicyRequest as UpdatePolicyModel,
)


@dataclass
class Policy:
    policy: dict

    def to_create_model(self, info: ConnectionInfo, token: str) -> CreatePolicyModel:
        return CreatePolicyModel(user_ip=str(info.user_ip), user_agent=info.user_agent, token=token, **self.__dict__)

    def to_update_model(self, id: str, info: ConnectionInfo, token: str) -> UpdatePolicyModel:
        return UpdatePolicyModel(
            id=id, user_ip=str(info.user_ip), user_agent=info.user_agent, token=token, **self.__dict__
        )


class PolicySchema(Schema):
    policy = fields.Dict(required=True)

    @post_load
    def make_class(self, data, **_kwargs) -> Policy:
        return Policy(**data)


class PolicyListSchema(Schema):
    policies = fields.List(cls_or_instance=fields.Dict(required=True), required=True)
    pagination = fields.Nested(PaginationResponseSchema, required=True)


@dataclass
class PolicyListRequest(RequestWithPagination):
    def to_model(self, info: ConnectionInfo, token: str) -> PolicyListModel:
        return PolicyListModel(user_ip=str(info.user_ip), user_agent=info.user_agent, token=token, **self.__dict__)


class PolicyListRequestSchema(PaginationSchema):
    @post_load
    def make_class(self, data, **_kwargs) -> PolicyListRequest:
        return PolicyListRequest(**data)


@dataclass
class PolicyRequest:
    id: str

    def to_model(self, info: ConnectionInfo, token: str) -> PolicyModel:
        return PolicyModel(user_ip=str(info.user_ip), user_agent=info.user_agent, token=token, **self.__dict__)


class PolicyRequestSchema(Schema):
    id = fields.Str(required=True)

    @post_load
    def make_class(self, data, **_kwargs) -> PolicyRequest:
        return PolicyRequest(**data)
