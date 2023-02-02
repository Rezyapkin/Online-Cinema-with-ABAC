from dataclasses import dataclass

from flasgger import Schema, fields
from marshmallow import post_load

from api.v1.schemas.connect_info import ConnectionInfo
from api.v1.schemas.pagination import PaginationSchema, RequestWithPagination, PaginationResponseSchema
from models.log_in_history import LogInHistoryRequest as LogInHistoryModel


@dataclass
class LogInHistoryRequest(RequestWithPagination):
    def to_model(self, info: ConnectionInfo, token: str) -> LogInHistoryModel:
        return LogInHistoryModel(user_ip=str(info.user_ip), user_agent=info.user_agent, token=token, **self.__dict__)


class LogInHistoryRequestSchema(PaginationSchema):
    @post_load
    def make_class(self, data, **_kwargs) -> LogInHistoryRequest:
        return LogInHistoryRequest(**data)


class LogInHistoryEntity(Schema):
    # fields.IP doesn't display by flasgger into OpenApi
    date_time = fields.DateTime(required=True)
    user_ip = fields.IP(required=True)
    user_agent = fields.Str(required=True)
    device = fields.Str(required=True)


class LogInHistoryResponseSchema(Schema):
    data = fields.Nested(LogInHistoryEntity, many=True, required=True)
    pagination = fields.Nested(PaginationResponseSchema, required=True)
