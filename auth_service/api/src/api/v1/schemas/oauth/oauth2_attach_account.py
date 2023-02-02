from dataclasses import dataclass

from flasgger import Schema, fields
from marshmallow import post_load

from models.oauth import OAuth2AttachAccountRequest as OAuth2AttachAccountModel
from api.v1.schemas.connect_info import ConnectionInfo


@dataclass
class OAuth2AttachAccount:
    code: str
    state: str

    def to_model(self, connection_info: ConnectionInfo, token: str) -> OAuth2AttachAccountModel:
        return OAuth2AttachAccountModel(
            user_ip=str(connection_info.user_ip),
            user_agent=connection_info.user_agent,
            token=token,
            code=self.code,
            state=self.state,
        )


class OAuth2AttachAccountSchema(Schema):
    code = fields.Str(required=True)
    state = fields.Str(required=True)

    @post_load
    def make_class(self, data, **_kwargs) -> OAuth2AttachAccount:
        return OAuth2AttachAccount(code=data["code"], state=data["state"])
