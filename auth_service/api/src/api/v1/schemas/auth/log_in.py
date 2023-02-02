from dataclasses import dataclass

from flasgger import Schema, fields
from marshmallow import post_load

from models.log_in import LogInRequest as LogInModel
from api.v1.schemas.connect_info import ConnectionInfo


@dataclass
class LogIn:
    email: str
    password: str

    def to_model(self, connection_info: ConnectionInfo) -> LogInModel:
        return LogInModel(ip=str(connection_info.user_ip), user_agent=connection_info.user_agent, **self.__dict__)


class LogInSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @post_load
    def email_to_lover_case(self, in_data, **_kwargs) -> LogIn:
        in_data["email"] = in_data["email"].lower()
        return LogIn(**in_data)
