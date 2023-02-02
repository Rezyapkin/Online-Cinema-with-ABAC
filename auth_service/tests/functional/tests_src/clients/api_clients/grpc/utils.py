import inspect
from enum import IntEnum
from functools import wraps
from typing import Callable, Any

import grpc
from grpc import StatusCode as GrpcStatus
from loguru import logger


class ErrorCode(IntEnum):
    INTERNAL_ERROR = 1
    UNAUTHENTICATED = 2
    INVALID_ARGUMENT = 3
    ALREADY_EXISTS = 4
    NOT_FOUND = 5

    @staticmethod
    def from_grpc(value: GrpcStatus):
        if value == GrpcStatus.INVALID_ARGUMENT:
            return ErrorCode.INVALID_ARGUMENT
        elif value == GrpcStatus.UNAUTHENTICATED:
            return ErrorCode.UNAUTHENTICATED
        elif value == GrpcStatus.ALREADY_EXISTS:
            return ErrorCode.ALREADY_EXISTS
        elif value == GrpcStatus.NOT_FOUND:
            return ErrorCode.NOT_FOUND
        else:
            return ErrorCode.INTERNAL_ERROR


def grpc_exception_into_error_code(func: Callable) -> Any:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)

            return func(*args, **kwargs)
        except grpc.RpcError as rpc_error:
            return ErrorCode.from_grpc(rpc_error.code())
        except Exception as e:
            logger.error("GRPC function {} failed!: {}".format(func.__name__, e))
            return ErrorCode.INTERNAL_ERROR

    return wrapper
