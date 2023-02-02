from dataclasses import dataclass

from flasgger import Schema, fields
from marshmallow import post_load

from api.v1.schemas.connect_info import ConnectionInfo
from api.v1.schemas.pagination import PaginationSchema, RequestWithPagination, PaginationResponseSchema
from models.user import UserListRequest as UserListModel
from models.user import UserRequest as UserModel


class OAuthAccount(Schema):
    provider = fields.Str(required=True)
    account_id = fields.Str(required=True)


class UserInfoSchema(Schema):
    id = fields.Str(required=True)
    email = fields.Email(required=True)
    is_active = fields.Bool(required=True)
    is_superuser = fields.Bool(required=True)
    oauth_accounts = fields.Nested(OAuthAccount, many=True, required=True)


class UserInfoInList(Schema):
    id = fields.Str(required=True)
    email = fields.Email(required=True)
    is_active = fields.Bool(required=True)
    is_superuser = fields.Bool(required=True)


class UserInfoListSchema(Schema):
    users = fields.Nested(UserInfoInList, many=True)
    pagination = fields.Nested(PaginationResponseSchema, required=True)


@dataclass
class UserRequest:
    id: str

    def to_model(self, info: ConnectionInfo, token: str) -> UserModel:
        return UserModel(user_ip=str(info.user_ip), user_agent=info.user_agent, token=token, **self.__dict__)


@dataclass
class UserListRequest(RequestWithPagination):
    def to_model(self, info: ConnectionInfo, token: str) -> UserListModel:
        return UserListModel(user_ip=str(info.user_ip), user_agent=info.user_agent, token=token, **self.__dict__)


class UserListRequestSchema(PaginationSchema):
    @post_load
    def make_class(self, data, **_kwargs) -> UserListRequest:
        return UserListRequest(**data)


class UserRequestSchema(Schema):
    id = fields.Str(required=True)

    @post_load
    def make_class(self, data, **_kwargs) -> UserRequest:
        return UserRequest(**data)
