from functools import lru_cache

from grpc_auth_service.oauth_service_pb2_grpc import GoogleOAuthStub

from services.oauth.base import BaseOAuthService
from services.utils.grpc_utils import get_grpc_channel


class GoogleOAuthService(BaseOAuthService):
    def get_stub(self):
        return GoogleOAuthStub(self.channel)


@lru_cache
def get_oauth_google_service():
    return GoogleOAuthService(get_grpc_channel())
