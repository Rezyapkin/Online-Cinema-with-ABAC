from dataclasses import dataclass

from models.common_request import CommonRequest


@dataclass
class UpdatePasswordRequest(CommonRequest):
    new_password: str
    old_password: str | None = None
