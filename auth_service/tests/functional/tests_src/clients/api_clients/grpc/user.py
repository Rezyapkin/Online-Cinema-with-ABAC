from ipaddress import ip_address
from datetime import datetime

from grpc_auth_service.user_service_pb2_grpc import UserStub

from tests_src.clients.api_clients.grpc.base import GrpcChannel, Metadata
from tests_src.clients.api_clients.grpc.utils import grpc_exception_into_error_code, ErrorCode
from tests_src.test_data.models.user import (
    LogInHistoryRequest,
    LogInHistory,
    SignUpRequest,
    SignUpResponse,
    LogInHistoryResponse,
)
from grpc_auth_service.user_service_pb2 import (
    CreateUserResponse,
    CreateUserRequest,
    GetUserLoginHistoryResponse,
    GetUserLoginHistoryRequest,
)


class GrpcUserClient:
    def __init__(self, channel: GrpcChannel):
        self._channel = channel.channel

    @grpc_exception_into_error_code
    async def create_user(self, request: SignUpRequest) -> SignUpResponse | ErrorCode:
        stub = UserStub(self._channel)

        response: CreateUserResponse = await stub.Create(
            CreateUserRequest(email=request.email, password=request.password),
            metadata=(
                (Metadata.IP_ADDRESS, str(request.ip)),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return SignUpResponse(
            email=response.email,
            id=response.id,
        )

    @grpc_exception_into_error_code
    async def get_log_in_history(
        self,
        request: LogInHistoryRequest,
    ) -> LogInHistoryResponse | ErrorCode:
        stub = UserStub(self._channel)

        response: GetUserLoginHistoryResponse = await stub.GetLoginHistory(
            GetUserLoginHistoryRequest(
                access_token=request.token,
                page_size=request.page_size,
                page_number=request.page_number,
            ),
            metadata=(
                (Metadata.IP_ADDRESS, str(request.user_ip)),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return LogInHistoryResponse(
            data=[
                LogInHistory(
                    user_ip=ip_address(i.ip_address),
                    date_time=datetime.fromisoformat(i.date),
                    user_agent=i.user_agent,
                    device=i.device,
                )
                for i in response.results
            ],
            total_count=response.total_count,
            total_pages=response.total_pages,
            prev_page=response.prev_page if response.prev_page else None,
            next_page=response.next_page if response.next_page else None,
        )
