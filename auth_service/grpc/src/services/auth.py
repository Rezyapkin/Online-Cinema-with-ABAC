from datetime import datetime

from sqlalchemy.exc import IntegrityError

from api.schemas.auth import (
    LoginEntryDto,
    LoginResulDto,
    RefreshTokenEntryDto,
    RefreshTokenResultDto,
    LogoutResultDto,
    LogoutEntryDto,
    LogoutOtherEntryDto,
    LogoutOtherResultDto,
    UpdatePasswordEntryDto,
    UpdatePasswordResultDto,
    UpdateEmailEntryDto,
    UpdateEmailResultDto,
    CheckTokenEntryDto,
    CheckTokenResultDto,
)
from services.login import LoginService, LoginRequestModel
from services.exceptions.exceptions import (
    UserPasswordInvalidError,
    UserPasswordUpdateSameError,
    UserEmailUpdateSameError,
    UserEmailCollisionError,
    BaseTokenError,
    UserDisabledError,
    UserNotFoundError,
)
from services.helpers.jwt_token import JwtPayload


# noinspection PyAttributeOutsideInit
class AuthService(LoginService):
    async def _disable_user(self, user_id: str, access_token: str, jwt_payload: JwtPayload):
        """Disable all user refresh tokens and blacklist current access."""
        await self.user_cache_manager.delete_user(user_id=user_id)
        await self.user_cache_manager.add_access_token_to_blacklist(
            access_token=access_token,
            expires_in=datetime.utcfromtimestamp(float(jwt_payload.exp)) - datetime.utcnow(),
        )
        # disable in history
        await self.login_history_manager.disable_user_sessions(user_id=user_id)

    async def login(self, entry_dto: LoginEntryDto) -> LoginResulDto:
        async with self.prepare():
            user = await self.user_manager.get_first_by(email=entry_dto.login)
            if not user:
                raise UserNotFoundError()

            if not self.user_manager.is_valid_password(user=user, password=entry_dto.password):
                raise UserPasswordInvalidError()

            auth_tokens = await self._login(
                LoginRequestModel(
                    user_id=user.id,
                    user_agent=entry_dto.user_agent,
                    ip_address=entry_dto.ip_address,
                )
            )

            return LoginResulDto(
                access_token=auth_tokens.access_token,
                refresh_token=auth_tokens.refresh_token,
                token_type=auth_tokens.token_type,
                expires_in=auth_tokens.expires_in,
            )

    async def refresh_token(self, entry_dto: RefreshTokenEntryDto) -> RefreshTokenResultDto:
        jwt_payload = await self.process_refresh_jwt(token=entry_dto.refresh_token, user_agent=entry_dto.user_agent)

        async with self.prepare():
            user = await self.user_manager.get(uuid=jwt_payload.user)
            if not user.is_active:
                raise UserDisabledError()

        tokens = await self._get_tokens(user_id=str(user.id), user_agent=entry_dto.user_agent)
        return RefreshTokenResultDto(**tokens.dict())

    async def logout(self, entry_dto: LogoutEntryDto) -> LogoutResultDto:
        jwt_payload = await self.process_access_jwt(token=entry_dto.access_token, user_agent=entry_dto.user_agent)

        async with self.prepare():
            # disable in cache
            await self.user_cache_manager.delete_user_by_user_agent(
                user_id=jwt_payload.user,
                user_agent=jwt_payload.user_agent,
            )
            await self.user_cache_manager.add_access_token_to_blacklist(
                access_token=entry_dto.access_token,
                expires_in=datetime.utcfromtimestamp(float(jwt_payload.exp)) - datetime.utcnow(),
            )
            # disable in history. Suppose latest is the correct entry
            user_login_history = await self.login_history_manager.get_first_by(
                user_id=jwt_payload.user,
                user_agent=jwt_payload.user_agent,
                order_by_creation=True,
            )
            await self.login_history_manager.update(db_obj=user_login_history, obj_in={"is_active": False})

        return LogoutResultDto()

    async def logout_other(self, entry_dto: LogoutOtherEntryDto) -> LogoutOtherResultDto:
        jwt_payload = await self.process_access_jwt(token=entry_dto.access_token, user_agent=entry_dto.user_agent)

        async with self.prepare():
            current_refresh_token = await self.user_cache_manager.get_user_by_user_agent(
                user_id=jwt_payload.user,
                user_agent=jwt_payload.user_agent,
            )

            all_auth = await self.user_cache_manager.get_user(user_id=jwt_payload.user)
            for user_agent, refresh_token in all_auth.items():
                if current_refresh_token != str(refresh_token):
                    await self.user_cache_manager.delete_user_by_user_agent(
                        user_id=jwt_payload.user, user_agent=user_agent
                    )

            # deactivate all sessions and activate latest on this user agent
            await self.login_history_manager.disable_user_sessions(user_id=jwt_payload.user)
            await self.login_history_manager.activate_latest_session(
                user_id=jwt_payload.user, user_agent=jwt_payload.user_agent
            )

        return LogoutOtherResultDto()

    async def update_password(self, entry_dto: UpdatePasswordEntryDto) -> UpdatePasswordResultDto:
        jwt_payload = await self.process_access_jwt(token=entry_dto.access_token, user_agent=entry_dto.user_agent)

        async with self.prepare():
            user = await self.user_manager.get(uuid=jwt_payload.user)

            if self.user_manager.is_valid_password(user=user, password=entry_dto.password):
                raise UserPasswordUpdateSameError()

            await self.user_manager.update(db_obj=user, obj_in={"hashed_password": entry_dto.password})
            await self._disable_user(
                user_id=jwt_payload.user, access_token=entry_dto.access_token, jwt_payload=jwt_payload
            )

        return UpdatePasswordResultDto()

    async def update_email(self, entry_dto: UpdateEmailEntryDto) -> UpdateEmailResultDto:
        jwt_payload = await self.process_access_jwt(token=entry_dto.access_token, user_agent=entry_dto.user_agent)

        async with self.prepare():
            user = await self.user_manager.get(uuid=jwt_payload.user)
            if entry_dto.email == user.email:
                raise UserEmailUpdateSameError()

            try:
                await self.user_manager.update(db_obj=user, obj_in={"email": entry_dto.email})
            except IntegrityError:
                raise UserEmailCollisionError()

            await self._disable_user(
                user_id=jwt_payload.user, access_token=entry_dto.access_token, jwt_payload=jwt_payload
            )

        return UpdateEmailResultDto()

    async def check_token(self, entry_dto: CheckTokenEntryDto) -> CheckTokenResultDto:
        result = False
        try:
            await self.process_access_jwt(token=entry_dto.access_token, user_agent=entry_dto.user_agent)
            result = True
        except BaseTokenError:
            pass

        return CheckTokenResultDto(success=result)
