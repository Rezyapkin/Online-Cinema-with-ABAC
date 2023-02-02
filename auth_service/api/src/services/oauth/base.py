from abc import ABC, abstractmethod

from grpc_auth_service.oauth_service_pb2 import (
    GetProviderLoginURLRequest,
    GetProviderLoginURLResponse,
    OAuthLoginRequest,
    OAuthLoginResponse,
    AttachAccountToUserRequest,
    DetachAccountFromUserRequest,
)

from models.status import Status, StatusCode
from models.token import TokenResponse
from models.common_request import CommonRequest
from models.oauth import GetLoginUrlResponse, GetLoginUrlRequest, OAuth2LogInRequest, OAuth2AttachAccountRequest
from services.base import BaseService
from services.utils.grpc_utils import handle_grpc_exception, Metadata


class BaseOAuthService(BaseService, ABC):
    @abstractmethod
    def get_stub(self):
        raise NotImplementedError()

    @handle_grpc_exception
    def get_provider_login_url(self, request: GetLoginUrlRequest) -> GetLoginUrlResponse | Status:
        response: GetProviderLoginURLResponse = self.stub.GetProviderLoginURL(
            GetProviderLoginURLRequest(callback_url=request.callback_url, access_token=request.token),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return GetLoginUrlResponse(url=response.url, state=response.state_token)

    @handle_grpc_exception
    def login(self, request: OAuth2LogInRequest) -> TokenResponse | Status:
        response: OAuthLoginResponse = self.stub.Login(
            OAuthLoginRequest(
                code=request.code,
                state_token=request.state,
            ),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
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
    def attach_account(self, request: OAuth2AttachAccountRequest) -> Status:
        self.stub.AttachAccountToUser(
            AttachAccountToUserRequest(
                code=request.code,
                access_token=request.token,
                state_token=request.state,
            ),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return Status(code=StatusCode.OK)

    @handle_grpc_exception
    def detach_account(self, request: CommonRequest) -> Status:
        self.stub.DetachAccountFromUser(
            DetachAccountFromUserRequest(
                access_token=request.token,
            ),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return Status(code=StatusCode.OK)
