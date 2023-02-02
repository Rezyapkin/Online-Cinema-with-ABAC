from grpc_auth_service.role_service_pb2_grpc import AdminRoleStub
from grpc_auth_service.role_service_pb2 import (
    GetUserRequest,
    GetUserResponse,
    GetUserListRequest,
    GetUserListResponse,
)

from tests_src.clients.api_clients.grpc.base import GrpcChannel
from tests_src.clients.api_clients.grpc.utils import grpc_exception_into_error_code, ErrorCode
from tests_src.test_data.models.admin import UserRequest, UserResponse, UserListRequest


class GrpcAdminClient:
    def __init__(self, channel: GrpcChannel, access_token: str):
        self._channel = channel.channel
        self._token = access_token

    @grpc_exception_into_error_code
    async def get_user(self, request: UserRequest) -> UserResponse | ErrorCode:
        stub = AdminRoleStub(self._channel)

        response: GetUserResponse = await stub.GetUser(GetUserRequest(access_token=self._token, id=request.user_id))

        return UserResponse(
            email=response.email, id=response.id, is_active=response.is_active, is_superuser=response.is_superuser
        )

    @grpc_exception_into_error_code
    async def get_user_list(
        self,
        request: UserListRequest,
    ) -> list[UserResponse] | ErrorCode:
        stub = AdminRoleStub(self._channel)

        response: GetUserListResponse = await stub.GetUserList(
            GetUserListRequest(
                access_token=self._token,
                offset=request.offset,
                limit=request.limit,
            ),
        )

        return [
            UserResponse(email=i.email, id=i.id, is_active=i.is_active, is_superuser=i.is_superuser)
            for i in response.results
        ]
