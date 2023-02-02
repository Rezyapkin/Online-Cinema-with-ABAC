from typing import Any

import grpc
import grpc_interceptor.exceptions
from pydantic import ValidationError

from api.grpc.base import BaseController
from api.schemas.oauth import (
    GetProviderLoginURLEntryDto,
    OAuthLoginEntryDto,
    AttachAccountToUserEntryDto,
    DetachAccountFromUserEntryDto,
)
from grpc_auth_service.oauth_service_pb2 import (
    GetProviderLoginURLRequest,
    GetProviderLoginURLResponse,
    OAuthLoginRequest,
    OAuthLoginResponse,
    AttachAccountToUserRequest,
    AttachAccountToUserResponse,
    DetachAccountFromUserRequest,
    DetachAccountFromUserResponse,
)
from grpc_auth_service.oauth_service_pb2_grpc import GoogleOAuthServicer

from services.exceptions.exceptions import UserDisabledError, BaseTokenError
from services.exceptions.oauth import (
    StateTokenIncorrectError,
    StatusTokenCollisionError,
    IncorrectResponseOAuthProviderError,
    UserProviderAccountCollisionError,
    UserProviderAccountNotAttachedError,
)
from services.oauth.google import GoogleOAuthService


class GoogleOAuthController(BaseController, GoogleOAuthServicer):
    def __init__(self, cache: Any, session_maker: Any):
        super().__init__(cache, session_maker)
        self.oauth_service = GoogleOAuthService(cache=self.cache, session_maker=self.session_maker)

    async def GetProviderLoginURL(
        self, request: GetProviderLoginURLRequest, context: grpc.aio.ServicerContext
    ) -> GetProviderLoginURLResponse:
        try:
            entry_dto = GetProviderLoginURLEntryDto(
                callback_url=request.callback_url,
                access_token=request.access_token,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            result_dto = await self.oauth_service.get_login_url(entry_dto=entry_dto)
        except BaseTokenError as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)

        return GetProviderLoginURLResponse(
            url=str(result_dto.url),
            state_token=result_dto.state_token,
        )

    async def Login(self, request: OAuthLoginRequest, context: grpc.aio.ServicerContext) -> OAuthLoginResponse:
        try:
            entry_dto = OAuthLoginEntryDto(
                code=request.code,
                state_token=request.state_token,
                user_agent=self.get_user_agent(context=context),
                ip_address=self.get_ip_address(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            result_dto = await self.oauth_service.login(entry_dto=entry_dto)
        except UserDisabledError as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)
        except (StateTokenIncorrectError, IncorrectResponseOAuthProviderError) as e:
            raise grpc_interceptor.exceptions.Internal(details=e.ERROR_MESSAGE)

        return OAuthLoginResponse(
            access_token=result_dto.access_token,
            refresh_token=result_dto.refresh_token,
            expires_in=result_dto.expires_in,
            token_type=result_dto.token_type,
        )

    async def AttachAccountToUser(
        self, request: AttachAccountToUserRequest, context: grpc.aio.ServicerContext
    ) -> AttachAccountToUserResponse:
        try:
            entry_dto = AttachAccountToUserEntryDto(
                code=request.code,
                state_token=request.state_token,
                access_token=request.access_token,
                user_agent=self.get_user_agent(context=context),
                ip_address=self.get_ip_address(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            await self.oauth_service.attach_account_to_user(entry_dto=entry_dto)
        except BaseTokenError as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)
        except (StateTokenIncorrectError, IncorrectResponseOAuthProviderError) as e:
            raise grpc_interceptor.exceptions.Internal(details=e.ERROR_MESSAGE)
        except UserProviderAccountCollisionError as e:
            raise grpc_interceptor.exceptions.AlreadyExists(details=e.ERROR_MESSAGE)
        except StatusTokenCollisionError as e:
            raise grpc_interceptor.exceptions.PermissionDenied(details=e.ERROR_MESSAGE)

        return AttachAccountToUserResponse()

    async def DetachAccountFromUser(
        self, request: DetachAccountFromUserRequest, context: grpc.aio.ServicerContext
    ) -> DetachAccountFromUserResponse:
        try:
            entry_dto = DetachAccountFromUserEntryDto(
                access_token=request.access_token,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            await self.oauth_service.detach_account_from_user(entry_dto=entry_dto)
        except BaseTokenError as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)
        except UserProviderAccountNotAttachedError as e:
            raise grpc_interceptor.exceptions.NotFound(details=e.ERROR_MESSAGE)

        return DetachAccountFromUserResponse()
