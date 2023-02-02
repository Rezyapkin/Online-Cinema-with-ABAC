from dataclasses import dataclass

from flasgger import Schema, fields
from marshmallow import post_load

from models.email import UpdateEmailRequest as UpdateEmailModel
from api.v1.schemas.connect_info import ConnectionInfo


@dataclass
class NewEmail:
    new_email: str
    password: str

    def to_model(self, connection_info: ConnectionInfo, token: str) -> UpdateEmailModel:
        return UpdateEmailModel(
            user_ip=str(connection_info.user_ip), user_agent=connection_info.user_agent, token=token, **self.__dict__
        )


class ChangeEmailSchema(Schema):
    password = fields.Str(required=True)
    new_email = fields.Email(required=True)

    @post_load
    def make_class(self, data, **_kwargs):
        return NewEmail(**data)
