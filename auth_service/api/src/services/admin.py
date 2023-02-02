from functools import lru_cache

import orjson

from grpc_auth_service.role_service_pb2 import (
    GetUserRequest,
    GetUserResponse,
    GetUserListRequest,
    GetUserListResponse,
    GetPolicyRequest,
    GetPolicyResponse,
    GetPolicyListRequest,
    GetPolicyListResponse,
    DeletePolicyRequest,
    CreatePolicyRequest,
    CreatePolicyResponse,
    UpdatePolicyRequest,
)
from grpc_auth_service.role_service_pb2_grpc import AdminRoleStub
from models.user import UserRequest, UserResponse, UserInList, UserListRequest, UserListResponse, OAuthAccount
from models.base import BasePagination
from models.policy import PolicyListRequest, PolicyRequest, PolicyResponse, PolicyListResponse
from models.policy import (
    CreatePolicyRequest as CreatePolicyRequestModel,
    CreatePolicyResponse as CreatePolicyResponseModel,
    UpdatePolicyRequest as UpdatePolicyRequestModel,
)
from models.status import StatusCode, Status
from models.status import Status
from services.base import BaseService
from services.utils.grpc_utils import get_grpc_channel, Metadata, handle_grpc_exception


class AdminService(BaseService):
    def get_stub(self):
        return AdminRoleStub(self.channel)

    @handle_grpc_exception
    def get_user(self, request: UserRequest) -> UserResponse | Status:
        response: GetUserResponse = self.stub.GetUser(
            GetUserRequest(id=request.id, access_token=request.token),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return UserResponse(
            email=response.email,
            id=response.id,
            is_active=response.is_active,
            is_superuser=response.is_superuser,
            oauth_accounts=[
                OAuthAccount(
                    account_id=item.account_id,
                    provider=item.provider,
                )
                for item in response.oauth_accounts
            ],
        )

    @handle_grpc_exception
    def get_user_list(self, request: UserListRequest) -> UserListResponse | Status:
        response: GetUserListResponse = self.stub.GetUserList(
            GetUserListRequest(
                access_token=request.token,
                page_number=request.page_number,
                page_size=request.page_size,
            ),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return UserListResponse(
            users=[
                UserInList(
                    email=user.email,
                    id=user.id,
                    is_active=user.is_active,
                    is_superuser=user.is_superuser,
                )
                for user in response.results
            ],
            pagination=BasePagination.instance_from(response),
        )

    @handle_grpc_exception
    def create_policy(self, request: CreatePolicyRequestModel) -> CreatePolicyResponseModel | Status:
        response: CreatePolicyResponse = self.stub.CreatePolicy(
            CreatePolicyRequest(policy=orjson.dumps(request.policy).decode("utf-8"), access_token=request.token),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return CreatePolicyResponseModel(
            id=response.id,
        )

    @handle_grpc_exception
    def get_policy(self, request: PolicyRequest) -> PolicyResponse | Status:
        response: GetPolicyResponse = self.stub.GetPolicy(
            GetPolicyRequest(id=request.id, access_token=request.token),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return PolicyResponse(
            policy=orjson.loads(response.policy),
        )

    @handle_grpc_exception
    def get_policy_list(self, request: PolicyListRequest) -> PolicyListResponse | Status:
        response: GetPolicyListResponse = self.stub.GetPolicyList(
            GetPolicyListRequest(
                access_token=request.token,
                page_number=request.page_number,
                page_size=request.page_size,
            ),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return PolicyListResponse(
            policies=[orjson.loads(policy) for policy in response.policy],
            pagination=BasePagination.instance_from(response),
        )

    @handle_grpc_exception
    def delete_policy(self, request: PolicyRequest) -> Status:
        self.stub.DeletePolicy(
            DeletePolicyRequest(id=request.id, access_token=request.token),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )

        return Status(code=StatusCode.OK)

    @handle_grpc_exception
    def update_policy(self, request: UpdatePolicyRequestModel) -> Status:
        self.stub.UpdatePolicy(
            UpdatePolicyRequest(
                id=request.id, policy=orjson.dumps(request.policy).decode("utf-8"), access_token=request.token
            ),
            metadata=(
                (Metadata.IP_ADDRESS, request.user_ip),
                (Metadata.USER_AGENT, request.user_agent),
            ),
        )
        return Status(code=StatusCode.OK)


@lru_cache
def get_admin_service():
    return AdminService(get_grpc_channel())
