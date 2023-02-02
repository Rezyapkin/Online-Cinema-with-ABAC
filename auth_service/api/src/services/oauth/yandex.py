from functools import lru_cache

from grpc_auth_service.oauth_service_pb2_grpc import YandexOAuthStub

from services.oauth.base import BaseOAuthService
from services.utils.grpc_utils import get_grpc_channel


class YandexOAuthService(BaseOAuthService):
    def get_stub(self):
        return YandexOAuthStub(self.channel)


@lru_cache
def get_oauth_yandex_service():
    return YandexOAuthService(get_grpc_channel())
