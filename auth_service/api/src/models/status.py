from dataclasses import dataclass
from enum import IntEnum
from http import HTTPStatus

from grpc import StatusCode as GrpcStatus


class StatusCode(IntEnum):
    OK = HTTPStatus.OK
    INTERNAL_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR
    UNAUTHENTICATED = HTTPStatus.UNAUTHORIZED
    INVALID_ARGUMENT = HTTPStatus.UNPROCESSABLE_ENTITY
    ALREADY_EXISTS = HTTPStatus.BAD_REQUEST
    NOT_FOUND = HTTPStatus.NOT_FOUND
    PERMISSION_DENIED = HTTPStatus.FORBIDDEN

    @staticmethod
    def from_grpc(value: GrpcStatus):
        grpc_status_code_mapping = {
            GrpcStatus.INVALID_ARGUMENT: StatusCode.INVALID_ARGUMENT,
            GrpcStatus.UNAUTHENTICATED: StatusCode.UNAUTHENTICATED,
            GrpcStatus.ALREADY_EXISTS: StatusCode.ALREADY_EXISTS,
            GrpcStatus.NOT_FOUND: StatusCode.NOT_FOUND,
            GrpcStatus.PERMISSION_DENIED: StatusCode.PERMISSION_DENIED,
        }

        return grpc_status_code_mapping.get(value, StatusCode.INTERNAL_ERROR)


@dataclass
class Status:
    code: StatusCode
    description: str | None = None
