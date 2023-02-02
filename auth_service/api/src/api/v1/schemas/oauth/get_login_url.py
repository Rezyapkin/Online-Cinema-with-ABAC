from dataclasses import dataclass

from api.v1.schemas.connect_info import ConnectionInfo
from models.oauth import GetLoginUrlRequest as GetLoginUrlRequestModel


@dataclass
class GetLoginUrlRequest:
    callback_url: str

    def to_model(self, info: ConnectionInfo, token: str | None = None) -> GetLoginUrlRequestModel:
        return GetLoginUrlRequestModel(
            user_ip=str(info.user_ip), user_agent=info.user_agent, token=token, **self.__dict__
        )
