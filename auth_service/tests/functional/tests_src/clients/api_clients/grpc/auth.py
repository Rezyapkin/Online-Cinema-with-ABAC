import grpc

from grpc_auth_service.auth_service_pb2 import (
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    RefreshTokenRequest,
    RefreshTokenResponse,
    UpdateUserPasswordRequest,
    UpdateUserEmailRequest,
)
from grpc_auth_service.auth_service_pb2_grpc import AuthStub

from tests_src.clients.api_clients.grpc.base import GrpcChannel, Metadata
from tests_src.clients.api_clients.grpc.utils import grpc_exception_into_error_code, ErrorCode
from tests_src.test_data.models.common import SuccessResponse
from tests_src.test_data.models.auth import (
    LogInRequest,
    CommonRequest,
    TokenResponse,
    ChangePasswordRequest,
    ChangeEmailRequest,
)


class GrpcAuthClient:
    def __init__(self, channel: GrpcChannel):
        self._channel = channel.channel

    @grpc_exception_into_error_code
    async def log_in(self, request: LogInRequest) -> TokenResponse | ErrorCode:
        stub = AuthStub(self._channel)
        response: LoginResponse = await stub.Login(
            LoginRequest(login=request.email, password=request.password),
            metadata=(
                (Metadata.IP_ADDRESS, str(request.ip)),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return TokenResponse(
            access_token=response.access_token,
            refresh_token=response.refresh_token,
            token_type=response.token_type,
            expires_in=response.expires_in,
        )

    @grpc_exception_into_error_code
    async def refresh_token(self, request: CommonRequest) -> TokenResponse | ErrorCode:
        stub = AuthStub(self._channel)

        response: RefreshTokenResponse = await stub.RefreshToken(
            RefreshTokenRequest(refresh_token=request.token),
            metadata=(
                (Metadata.IP_ADDRESS, str(request.user_ip)),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return TokenResponse(
            access_token=response.access_token,
            refresh_token=response.access_token,
            token_type=response.token_type,
            expires_in=response.expires_in,
        )

    @grpc_exception_into_error_code
    async def log_out(self, request: CommonRequest) -> SuccessResponse | ErrorCode:
        stub = AuthStub(self._channel)
        await stub.Logout(
            LogoutRequest(access_token=request.token),
            metadata=(
                (Metadata.IP_ADDRESS, str(request.user_ip)),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return SuccessResponse()

    @grpc_exception_into_error_code
    async def change_password(self, request: ChangePasswordRequest) -> SuccessResponse | ErrorCode:
        stub = AuthStub(self._channel)

        await stub.UpdatePassword(
            UpdateUserPasswordRequest(access_token=request.token, password=request.new_password),
            metadata=(
                (Metadata.IP_ADDRESS, str(request.user_ip)),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return SuccessResponse()

    @grpc_exception_into_error_code
    async def change_email(self, request: ChangeEmailRequest) -> SuccessResponse | ErrorCode:
        stub = AuthStub(self._channel)

        await stub.UpdateEmail(
            UpdateUserEmailRequest(access_token=request.token, email=request.new_email),
            metadata=(
                (Metadata.IP_ADDRESS, str(request.user_ip)),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return SuccessResponse()

    async def ping(self) -> bool:
        stub = AuthStub(self._channel)
        try:
            await stub.Logout(LogoutRequest(access_token="1234"))
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.UNAUTHENTICATED:
                return True
        return False
