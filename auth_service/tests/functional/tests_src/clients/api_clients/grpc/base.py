from enum import Enum

import grpc
from grpc_auth_service.utils import Metadata as CustomMetadata
from pydantic import AnyUrl


class Metadata(str, Enum):
    IP_ADDRESS = CustomMetadata.IP_ADDRESS
    USER_AGENT = CustomMetadata.USER_AGENT


class GrpcChannel:
    def __init__(self, dsn: AnyUrl):
        self._channel = None
        channel_options = [
            ("grpc.lb_policy_name", "pick_first"),
            ("grpc.enable_retries", 0),
            ("grpc.keepalive_timeout_ms", 10000),
        ]
        self._channel = grpc.aio.insecure_channel(dsn, options=channel_options)

    @property
    def channel(self) -> grpc.aio.Channel:
        return self._channel
