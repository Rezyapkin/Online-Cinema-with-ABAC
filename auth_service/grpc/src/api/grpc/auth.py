import grpc
import grpc_interceptor.exceptions
from pydantic import ValidationError

from api.grpc.base import BaseController
from api.schemas.auth import (
    LoginEntryDto,
    RefreshTokenEntryDto,
    LogoutEntryDto,
    LogoutOtherEntryDto,
    UpdatePasswordEntryDto,
    UpdateEmailEntryDto,
    CheckTokenEntryDto,
)
from grpc_auth_service.auth_service_pb2 import (
    LoginRequest,
    LoginResponse,
    RefreshTokenResponse,
    RefreshTokenRequest,
    LogoutRequest,
    LogoutResponse,
    UpdateUserPasswordRequest,
    UpdateUserPasswordResponse,
    UpdateUserEmailRequest,
    UpdateUserEmailResponse,
    CheckTokenRequest,
    CheckTokenResponse,
)
from grpc_auth_service.auth_service_pb2_grpc import AuthServicer
from services.auth import AuthService
from services.exceptions.exceptions import (
    UserPasswordInvalidError,
    BaseTokenError,
    UserPasswordUpdateSameError,
    UserEmailUpdateSameError,
    UserEmailCollisionError,
    UserDisabledError,
    UserNotFoundError,
)


class AuthController(BaseController, AuthServicer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_service: AuthService = AuthService(cache=self.cache, session_maker=self.session_maker)

    async def Login(self, request: LoginRequest, context: grpc.aio.ServicerContext) -> LoginResponse:
        try:
            entry_dto = LoginEntryDto(
                login=request.login,
                password=request.password,
                user_agent=self.get_user_agent(context=context),
                ip_address=self.get_ip_address(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            result_dto = await self.auth_service.login(entry_dto=entry_dto)
        except UserNotFoundError as e:
            raise grpc_interceptor.exceptions.NotFound(details=e.ERROR_MESSAGE)
        except (UserDisabledError, UserPasswordInvalidError) as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)

        return LoginResponse(
            access_token=result_dto.access_token,
            refresh_token=result_dto.refresh_token,
            expires_in=result_dto.expires_in,
            token_type=result_dto.token_type,
        )

    async def RefreshToken(
        self, request: RefreshTokenRequest, context: grpc.aio.ServicerContext
    ) -> RefreshTokenResponse:
        try:
            entry_dto = RefreshTokenEntryDto(
                refresh_token=request.refresh_token,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            result_dto = await self.auth_service.refresh_token(entry_dto=entry_dto)
        except (BaseTokenError, UserDisabledError) as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)

        return RefreshTokenResponse(
            access_token=result_dto.access_token,
            refresh_token=result_dto.refresh_token,
            expires_in=result_dto.expires_in,
            token_type=result_dto.token_type,
        )

    async def Logout(self, request: LogoutRequest, context: grpc.aio.ServicerContext) -> LogoutResponse:
        try:
            entry_dto = LogoutEntryDto(
                access_token=request.access_token,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            await self.auth_service.logout(entry_dto=entry_dto)
        except BaseTokenError as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)

        return LogoutResponse()

    async def LogoutOther(self, request: LogoutRequest, context: grpc.aio.ServicerContext) -> LogoutResponse:
        try:
            entry_dto = LogoutOtherEntryDto(
                access_token=request.access_token,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            await self.auth_service.logout_other(entry_dto=entry_dto)
        except BaseTokenError as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)

        return LogoutResponse()

    async def UpdatePassword(
        self, request: UpdateUserPasswordRequest, context: grpc.aio.ServicerContext
    ) -> UpdateUserPasswordResponse:
        try:
            entry_dto = UpdatePasswordEntryDto(
                access_token=request.access_token,
                password=request.password,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            await self.auth_service.update_password(entry_dto=entry_dto)
        except BaseTokenError as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)
        except UserPasswordUpdateSameError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=e.ERROR_MESSAGE)

        return UpdateUserPasswordResponse()

    async def UpdateEmail(
        self, request: UpdateUserEmailRequest, context: grpc.aio.ServicerContext
    ) -> UpdateUserEmailResponse:
        try:
            entry_dto = UpdateEmailEntryDto(
                access_token=request.access_token,
                email=request.email,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        try:
            await self.auth_service.update_email(entry_dto=entry_dto)
        except BaseTokenError as e:
            raise grpc_interceptor.exceptions.Unauthenticated(details=e.ERROR_MESSAGE)
        except UserEmailUpdateSameError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=e.ERROR_MESSAGE)
        except UserEmailCollisionError as e:
            raise grpc_interceptor.exceptions.AlreadyExists(details=e.ERROR_MESSAGE)

        return UpdateUserEmailResponse()

    async def CheckToken(self, request: CheckTokenRequest, context: grpc.aio.ServicerContext) -> CheckTokenResponse:
        try:
            entry_dto = CheckTokenEntryDto(
                access_token=request.access_token,
                user_agent=self.get_user_agent(context=context),
            )
        except ValidationError as e:
            raise grpc_interceptor.exceptions.InvalidArgument(details=str(e))

        result_dto = await self.auth_service.check_token(entry_dto=entry_dto)

        return CheckTokenResponse(success=result_dto.success)
