from dataclasses import dataclass

from flasgger import Schema, fields
from marshmallow import validate, post_load

from api.v1.schemas.connect_info import ConnectionInfo
from models.sign_up import SignUpRequest as SignUpModel
from api.v1.schemas.auth import PASSWORD_MIN_SYMBOLS


@dataclass
class SignUp:
    email: str
    password: str

    def to_model(self, connection_info: ConnectionInfo) -> SignUpModel:
        return SignUpModel(
            ip=str(connection_info.user_ip),
            user_agent=connection_info.user_agent,
            **self.__dict__,
        )


class SignUpSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=validate.Length(
            min=PASSWORD_MIN_SYMBOLS, error="Password length should be bigger than {min} symbols."
        ),
    )

    @post_load
    def email_to_lover_case(self, in_data, **_kwargs) -> SignUp:
        in_data["email"] = in_data["email"].lower()
        return SignUp(**in_data)


class SignUpResponseSchema(Schema):
    email = fields.Email(required=True)
    id = fields.Str(required=True)
