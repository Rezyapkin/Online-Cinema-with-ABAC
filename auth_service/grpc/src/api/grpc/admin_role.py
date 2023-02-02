import grpc
import grpc_interceptor.exceptions
from pydantic import ValidationError

from api.grpc.base import BaseController
from api.schemas.admin_role import (
    GetUserEntryDto,
    GetUserListEntryDto,
    CreatePolicyEntryDto,
    GetPolicyEntryDto,
    GetPolicyListEntryDto,
    DeletePolicyEntryDto,
    UpdatePolicyEntryDto,
    CheckAccessEntryDto,
)
from grpc_auth_service.role_service_pb2 import (
    GetUserRequest,
    GetUserResponse,
    GetUserListRequest,
    GetUserListResponse,
    UserInList,
    CreatePolicyRequest,
    CreatePolicyResponse,
    GetPolicyRequest,
    GetPolicyResponse,
    GetPolicyListRequest,
    GetPolicyListResponse,
    DeletePolicyRequest,
    DeletePolicyResponse,
    UpdatePolicyRequest,
    UpdatePolicyResponse,
    CheckAccessResponse,
    CheckAccessRequest,
    AnyUserOAuthProviderAccount,
)
from grpc_auth_service.role_service_pb2_grpc import AdminRoleServicer

from services.exceptions.exceptions import (
    BaseTokenError,
    UserNotFoundError,
    UserNotSuperuserError,
    PolicyBadFormattedError,
    PolicyAlreadyExistsError,
    PolicyNotFoundError,
    PolicyListPageNotFoundError,
    UserListPageNotFoundError,
)
from services.admin_role import AdminRoleService


class AdminRoleController(BaseController, AdminRoleServicer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.admin_role_service: AdminRoleService = AdminRoleService(cache=self.cache, session_maker=self.session_maker)

    async def GetUser(self, request: GetUserRequest, context: grpc.aio.ServicerContext) -> GetUserResponse:
        try:
            entry_dto = GetUserEntryDto(
                access_token=request.access_token,
                id=request.id,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            result_dto = await self.admin_role_service.get_user(entry_dto=entry_dto)
        except (BaseTokenError, UserNotSuperuserError) as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)
        except UserNotFoundError as e:
            raise grpc_interceptor.exceptions.NotFound(details=e.ERROR_MESSAGE)

        return GetUserResponse(
            id=str(result_dto.id),
            email=result_dto.email,
            is_active=result_dto.is_active,
            is_superuser=result_dto.is_superuser,
            oauth_accounts=[
                AnyUserOAuthProviderAccount(provider=item.provider, account_id=item.account_id)
                for item in result_dto.oauth_accounts
            ],
        )

    async def GetUserList(self, request: GetUserListRequest, context: grpc.aio.ServicerContext) -> GetUserListResponse:
        try:
            entry_dto = GetUserListEntryDto(
                access_token=request.access_token,
                page_number=request.page_number,
                page_size=request.page_size,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            result_dto = await self.admin_role_service.get_user_list(entry_dto=entry_dto)
        except (BaseTokenError, UserNotSuperuserError) as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)
        except UserListPageNotFoundError as e:
            raise grpc_interceptor.exceptions.NotFound(details=e.ERROR_MESSAGE)

        return GetUserListResponse(
            results=[
                UserInList(
                    id=str(result.id),
                    email=result.email,
                    is_active=result.is_active,
                    is_superuser=result.is_superuser,
                )
                for result in result_dto.results
            ],
            total_count=result_dto.total_count,
            prev_page=result_dto.prev_page,
            next_page=result_dto.next_page,
            total_pages=result_dto.total_pages,
        )

    async def CreatePolicy(
        self, request: CreatePolicyRequest, context: grpc.aio.ServicerContext
    ) -> CreatePolicyResponse:
        try:
            entry_dto = CreatePolicyEntryDto(
                access_token=request.access_token,
                policy=request.policy,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            result_dto = await self.admin_role_service.create_policy(entry_dto=entry_dto)
        except (BaseTokenError, UserNotSuperuserError) as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)
        except PolicyBadFormattedError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=e.ERROR_MESSAGE)
        except PolicyAlreadyExistsError as e:
            raise grpc_interceptor.exceptions.AlreadyExists(details=e.ERROR_MESSAGE)

        return CreatePolicyResponse(id=str(result_dto.id))

    async def UpdatePolicy(
        self, request: UpdatePolicyRequest, context: grpc.aio.ServicerContext
    ) -> UpdatePolicyResponse:
        try:
            entry_dto = UpdatePolicyEntryDto(
                access_token=request.access_token,
                id=request.id,
                policy=request.policy,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            await self.admin_role_service.update_policy(entry_dto=entry_dto)
        except (BaseTokenError, UserNotSuperuserError) as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)
        except PolicyBadFormattedError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=e.ERROR_MESSAGE)
        except PolicyAlreadyExistsError as e:
            raise grpc_interceptor.exceptions.AlreadyExists(details=e.ERROR_MESSAGE)
        except PolicyNotFoundError as e:
            raise grpc_interceptor.exceptions.NotFound(details=e.ERROR_MESSAGE)

        return UpdatePolicyResponse()

    async def DeletePolicy(
        self, request: DeletePolicyRequest, context: grpc.aio.ServicerContext
    ) -> DeletePolicyResponse:
        try:
            entry_dto = DeletePolicyEntryDto(
                access_token=request.access_token,
                id=request.id,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            await self.admin_role_service.delete_policy(entry_dto=entry_dto)
        except (BaseTokenError, UserNotSuperuserError) as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)
        except PolicyNotFoundError as e:
            raise grpc_interceptor.exceptions.NotFound(details=e.ERROR_MESSAGE)

        return DeletePolicyResponse()

    async def GetPolicy(self, request: GetPolicyRequest, context: grpc.aio.ServicerContext) -> GetPolicyResponse:
        try:
            entry_dto = GetPolicyEntryDto(
                access_token=request.access_token,
                id=request.id,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            result_dto = await self.admin_role_service.get_policy(entry_dto=entry_dto)
        except (BaseTokenError, UserNotSuperuserError) as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)
        except PolicyNotFoundError as e:
            raise grpc_interceptor.exceptions.NotFound(details=e.ERROR_MESSAGE)

        return GetPolicyResponse(policy=result_dto.policy)

    async def GetPolicyList(
        self, request: GetPolicyListRequest, context: grpc.aio.ServicerContext
    ) -> GetPolicyListResponse:
        try:
            entry_dto = GetPolicyListEntryDto(
                access_token=request.access_token,
                page_number=request.page_number,
                page_size=request.page_size,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            result_dto = await self.admin_role_service.get_policy_list(entry_dto=entry_dto)
        except (BaseTokenError, UserNotSuperuserError) as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)
        except PolicyListPageNotFoundError as e:
            raise grpc_interceptor.exceptions.NotFound(details=e.ERROR_MESSAGE)

        return GetPolicyListResponse(
            policy=result_dto.policy,
            total_count=result_dto.total_count,
            prev_page=result_dto.prev_page,
            next_page=result_dto.next_page,
            total_pages=result_dto.total_pages,
        )

    async def CheckAccess(self, request: CheckAccessRequest, context: grpc.aio.ServicerContext) -> CheckAccessResponse:
        try:
            entry_dto = CheckAccessEntryDto(
                access_token=request.access_token,
                inquiry=request.inquiry,
                user_agent=self.get_user_agent(context=context),
                ip=self.get_ip_address(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        result_dto = await self.admin_role_service.check_access(entry_dto=entry_dto)

        return CheckAccessResponse(has_access=result_dto.has_access)
