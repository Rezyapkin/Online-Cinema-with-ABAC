from tests_src.clients.api_clients.grpc.base import GrpcChannel
from tests_src.clients.api_clients.grpc.auth import GrpcAuthClient
from tests_src.clients.api_clients.grpc.admin import GrpcAdminClient
from tests_src.clients.api_clients.grpc.user import GrpcUserClient


class GrpcClient:
    def __init__(self, channel: GrpcChannel):
        self.auth = GrpcAuthClient(channel)
        self.admin = GrpcAdminClient(channel, "")
        self.user = GrpcUserClient(channel)
