from typing import Any

import grpc
import grpc_interceptor.exceptions
from pydantic import ValidationError

from api.grpc.base import BaseController
from api.schemas.user import CreateEntryDto, GetUserLoginHistoryEntryDto, GetUserMeEntryDto
from grpc_auth_service.user_service_pb2 import (
    CreateUserRequest,
    CreateUserResponse,
    GetUserLoginHistoryRequest,
    UserLoginHistory,
    GetUserLoginHistoryResponse,
    GetUserMeRequest,
    GetUserMeResponse,
    UserOAuthProviderAccount,
)
from grpc_auth_service.user_service_pb2_grpc import UserServicer
from services.exceptions.exceptions import UserEmailCollisionError, BaseTokenError, UserHistoryPageNotFoundError
from services.user import UserService


class UserController(BaseController, UserServicer):
    def __init__(self, cache: Any, session_maker: Any):
        super().__init__(cache, session_maker)
        self.user_service: UserService = UserService(cache=self.cache, session_maker=self.session_maker)

    async def Create(self, request: CreateUserRequest, context: grpc.aio.ServicerContext) -> CreateUserResponse:
        try:
            entry_dto = CreateEntryDto(
                email=request.email,
                password=request.password,
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            result_dto = await self.user_service.create(entry_dto=entry_dto)
        except UserEmailCollisionError as e:
            raise grpc_interceptor.exceptions.AlreadyExists(details=e.ERROR_MESSAGE)

        return CreateUserResponse(
            id=str(result_dto.uuid),
            email=result_dto.email,
        )

    async def GetLoginHistory(
        self, request: GetUserLoginHistoryRequest, context: grpc.aio.ServicerContext
    ) -> GetUserLoginHistoryResponse:
        try:
            entry_dto = GetUserLoginHistoryEntryDto(
                access_token=request.access_token,
                page_number=request.page_number,
                page_size=request.page_size,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            result_dto = await self.user_service.get_login_history(entry_dto=entry_dto)
        except BaseTokenError as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)
        except UserHistoryPageNotFoundError as e:
            raise grpc_interceptor.exceptions.NotFound(details=e.ERROR_MESSAGE)

        return GetUserLoginHistoryResponse(
            results=[
                UserLoginHistory(
                    date=str(result.date),
                    device=result.device,
                    ip_address=result.ip_address,
                    user_agent=result.user_agent,
                )
                for result in result_dto.results
            ],
            total_count=result_dto.total_count,
            prev_page=result_dto.prev_page,
            next_page=result_dto.next_page,
            total_pages=result_dto.total_pages,
        )

    async def GetUserMe(self, request: GetUserMeRequest, context: grpc.aio.ServicerContext) -> GetUserMeResponse:
        try:
            entry_dto = GetUserMeEntryDto(
                access_token=request.access_token,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            result_dto = await self.user_service.get_user_me(entry_dto=entry_dto)
        except BaseTokenError as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)

        return GetUserMeResponse(
            email=result_dto.email,
            oauth_accounts=[
                UserOAuthProviderAccount(provider=item.provider, account_id=item.account_id)
                for item in result_dto.oauth_accounts
            ],
        )
