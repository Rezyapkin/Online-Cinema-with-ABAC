from enum import Enum
from typing import Callable, Any
from functools import wraps

import grpc
from grpc import Channel as GrpcChannel
from grpc_auth_service.utils import Metadata as CustomMetadata
from functools import lru_cache
from loguru import logger

from models.status import StatusCode, Status


def handle_grpc_exception(func: Callable) -> Any:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except grpc.RpcError as rpc_error:
            code = StatusCode.from_grpc(rpc_error.code())
            return Status(
                code=code,
                description="Internal Error" if code == StatusCode.INTERNAL_ERROR else rpc_error.details(),
            )
        except Exception as e:
            logger.exception("GRPC function {} failed!: {}".format(func.__name__, e))
            return Status(
                code=StatusCode.INTERNAL_ERROR,
                description="Internal error",
            )

    return wrapper


class Metadata(str, Enum):
    IP_ADDRESS = CustomMetadata.IP_ADDRESS
    USER_AGENT = CustomMetadata.USER_AGENT


grpc_channel: GrpcChannel | None = None


@lru_cache
def get_grpc_channel() -> GrpcChannel:
    return grpc_channel
