from dataclasses import dataclass

from flasgger import Schema, fields
from marshmallow import post_load

from models.oauth import OAuth2LogInRequest as OAuth2LogInModel
from api.v1.schemas.connect_info import ConnectionInfo


@dataclass
class OAuth2LogIn:
    code: str
    state: str

    def to_model(self, connection_info: ConnectionInfo) -> OAuth2LogInModel:
        return OAuth2LogInModel(
            user_ip=str(connection_info.user_ip),
            user_agent=connection_info.user_agent,
            code=self.code,
            state=self.state,
        )


class OAuth2LogInSchema(Schema):
    code = fields.Str(required=True)
    state = fields.Str(required=True)

    @post_load
    def make_class(self, data, **_kwargs) -> OAuth2LogIn:
        return OAuth2LogIn(code=data["code"], state=data["state"])
