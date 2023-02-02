from dataclasses import dataclass

from models.common_request import CommonRequest


@dataclass
class UpdateEmailRequest(CommonRequest):
    new_email: str
    password: str | None = None
