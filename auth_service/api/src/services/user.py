from ipaddress import ip_address
from datetime import datetime
from functools import lru_cache


from grpc_auth_service.user_service_pb2 import (
    CreateUserRequest,
    CreateUserResponse,
    GetUserLoginHistoryResponse,
    GetUserLoginHistoryRequest,
    GetUserMeRequest,
    GetUserMeResponse,
)
from grpc_auth_service.user_service_pb2_grpc import UserStub

from models.base import BasePagination
from models.sign_up import SignUpRequest, SignUpResponse
from models.log_in_history import LogInHistoryRequest, LogInHistoryResponse, LogInHistoryItem
from models.status import Status
from models.user import UserMeResponse, OAuthAccount
from models.common_request import CommonRequest
from services.base import BaseService
from services.utils.grpc_utils import get_grpc_channel, Metadata, handle_grpc_exception


class UserService(BaseService):
    def get_stub(self):
        return UserStub(self.channel)

    @handle_grpc_exception
    def create_user(self, request: SignUpRequest) -> SignUpResponse | Status:
        response: CreateUserResponse = self.stub.Create(
            CreateUserRequest(email=request.email, password=request.password),
            metadata=(
                (Metadata.IP_ADDRESS, request.ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return SignUpResponse(
            email=response.email,
            id=response.id,
        )

    @handle_grpc_exception
    def get_log_in_history(
        self,
        request: LogInHistoryRequest,
    ) -> Status | LogInHistoryResponse:
        response: GetUserLoginHistoryResponse = self.stub.GetLoginHistory(
            GetUserLoginHistoryRequest(
                access_token=request.token,
                page_number=request.page_number,
                page_size=request.page_size,
            ),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return LogInHistoryResponse(
            data=[
                LogInHistoryItem(
                    user_ip=ip_address(item.ip_address),
                    date_time=datetime.fromisoformat(item.date),
                    user_agent=item.user_agent,
                    device=item.device,
                )
                for item in response.results
            ],
            pagination=BasePagination.instance_from(response),
        )

    @handle_grpc_exception
    def get_user_me(self, request: CommonRequest) -> UserMeResponse | Status:
        response: GetUserMeResponse = self.stub.GetUserMe(
            GetUserMeRequest(access_token=request.token),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return UserMeResponse(
            email=response.email,
            oauth_accounts=[
                OAuthAccount(
                    account_id=item.account_id,
                    provider=item.provider,
                )
                for item in response.oauth_accounts
            ],
        )


@lru_cache
def get_user_service():
    return UserService(get_grpc_channel())
