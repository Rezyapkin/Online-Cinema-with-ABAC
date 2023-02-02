from dataclasses import dataclass

from flasgger import Schema, fields
from marshmallow import ValidationError, post_load

from models.password import UpdatePasswordRequest as UpdatePasswordModel
from api.v1.schemas.connect_info import ConnectionInfo
from api.v1.schemas.auth import PASSWORD_MIN_SYMBOLS


@dataclass
class Password:
    password: str

    def to_model(self, connection_info: ConnectionInfo, token: str) -> UpdatePasswordModel:
        return UpdatePasswordModel(
            token=token,
            user_ip=str(connection_info.user_ip),
            user_agent=connection_info.user_agent,
            new_password=self.password,
        )


class ChangePasswordSchema(Schema):
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True)
    new_password_confirm = fields.Str(required=True)

    @post_load
    def check_passwords(self, in_data: dict, **_kwargs) -> Password:
        new_one = in_data["new_password"]
        old_one = in_data["old_password"]
        new_another = in_data["new_password_confirm"]

        if len(new_one) < PASSWORD_MIN_SYMBOLS:
            raise ValidationError(f"Password length should be bigger than {PASSWORD_MIN_SYMBOLS} symbols.")

        if new_one == old_one:
            raise ValidationError("Old password is equal to new password.")

        if new_one != new_another:
            raise ValidationError("Password confirmation isn't equal to new password")

        return Password(password=new_one)
