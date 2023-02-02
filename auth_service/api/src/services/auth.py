from functools import lru_cache

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
from models.log_in import LogInRequest
from models.common_request import CommonRequest
from models.token import TokenResponse
from models.status import StatusCode, Status
from models.password import UpdatePasswordRequest
from models.email import UpdateEmailRequest
from services.base import BaseService
from services.utils.grpc_utils import get_grpc_channel, Metadata, handle_grpc_exception


class AuthService(BaseService):
    def get_stub(self):
        return AuthStub(self.channel)

    @handle_grpc_exception
    def log_in(self, request: LogInRequest) -> TokenResponse | Status:
        response: LoginResponse = self.stub.Login(
            LoginRequest(login=request.email, password=request.password),
            metadata=(
                (Metadata.IP_ADDRESS, request.ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return TokenResponse(
            access_token=response.access_token,
            refresh_token=response.refresh_token,
            token_type=response.token_type,
            expires_in=response.expires_in,
        )

    @handle_grpc_exception
    def refresh_token(self, request: CommonRequest) -> TokenResponse | Status:
        response: RefreshTokenResponse = self.stub.RefreshToken(
            RefreshTokenRequest(refresh_token=request.token),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return TokenResponse(
            access_token=response.access_token,
            refresh_token=response.access_token,
            token_type=response.token_type,
            expires_in=response.expires_in,
        )

    @handle_grpc_exception
    def log_out(self, request: CommonRequest) -> Status:
        self.stub.Logout(
            LogoutRequest(access_token=request.token),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return Status(code=StatusCode.OK)

    @handle_grpc_exception
    def change_password(self, request: UpdatePasswordRequest) -> Status:
        self.stub.UpdatePassword(
            UpdateUserPasswordRequest(access_token=request.token, password=request.new_password),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return Status(code=StatusCode.OK)

    @handle_grpc_exception
    def change_email(self, request: UpdateEmailRequest) -> Status:
        self.stub.UpdateEmail(
            UpdateUserEmailRequest(access_token=request.token, email=request.new_email),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return Status(code=StatusCode.OK)


@lru_cache
def get_auth_service():
    return AuthService(get_grpc_channel())
