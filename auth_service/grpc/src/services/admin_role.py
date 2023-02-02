from contextlib import asynccontextmanager
from typing import Any

from grpc_auth_service.utils import Constants
from loguru import logger
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from api.schemas.admin_role import (
    GetUserEntryDto,
    GetUserResultDto,
    GetUserListEntryDto,
    GetUserListResultDto,
    UserInList,
    CreatePolicyEntryDto,
    CreatePolicyResultDto,
    GetPolicyEntryDto,
    GetPolicyResultDto,
    GetPolicyListEntryDto,
    GetPolicyListResultDto,
    DeletePolicyEntryDto,
    DeletePolicyResultDto,
    UpdatePolicyEntryDto,
    UpdatePolicyResultDto,
    CheckAccessEntryDto,
    CheckAccessResultDto,
    AnyUserOAuthProviderAccountDto,
)
from api.schemas.base import BasePaginationResultDto
from db.storage.postgres.abac import ABACCrudStorage
from db.storage.postgres.user import UserCrudStorage
from db.storage.postgres.oauth import UserOAuthAccountCrudStorage
from models.base import BaseOrjsonModel
from models.postgres.abac import PolicyModelSchema
from services.abac.guard import Guard, Inquiry
from services.abac.policy import Policy
from services.base import BaseService
from services.exceptions.exceptions import (
    UserNotFoundError,
    UserNotSuperuserError,
    PolicyBadFormattedError,
    PolicyAlreadyExistsError,
    PolicyNotFoundError,
    BaseTokenError,
    PolicyListPageNotFoundError,
    UserListPageNotFoundError,
)


class UserSubject(BaseOrjsonModel):
    is_user: bool
    is_superuser: bool


# noinspection PyAttributeOutsideInit
class AdminRoleService(BaseService):
    @asynccontextmanager
    async def prepare(self) -> None:
        async with self.session_maker() as session:
            self.user_manager: UserCrudStorage = UserCrudStorage(client=session)
            self.abac_pip_manager: ABACCrudStorage = ABACCrudStorage(client=session)
            self.abac_pdp_manager: Guard = Guard(storage=self.abac_pip_manager)
            self.user_oauth_account_manager: UserOAuthAccountCrudStorage = UserOAuthAccountCrudStorage(client=session)

            yield

    async def _check_super_user(self, admin_id: str) -> None:
        admin = await self.user_manager.get(uuid=admin_id)
        if admin.is_active is False or admin.is_superuser is False:
            raise UserNotSuperuserError()

    async def get_user(self, entry_dto: GetUserEntryDto) -> GetUserResultDto:
        jwt_payload = await self.process_access_jwt(token=entry_dto.access_token, user_agent=entry_dto.user_agent)

        async with self.prepare():
            await self._check_super_user(admin_id=jwt_payload.user)
            user = await self.user_manager.get(uuid=str(entry_dto.id))

            if not user:
                raise UserNotFoundError()

            oauth_accounts = await self.user_oauth_account_manager.get_user_oauth_accounts(
                user_id=jwt_payload.user,
            )

        return GetUserResultDto(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            oauth_accounts=[
                AnyUserOAuthProviderAccountDto(
                    provider=item.oauth_provider_name,
                    account_id=item.oauth_account_id,
                )
                for item in oauth_accounts
            ],
        )

    async def get_user_list(self, entry_dto: GetUserListEntryDto) -> GetUserListResultDto:
        jwt_payload = await self.process_access_jwt(token=entry_dto.access_token, user_agent=entry_dto.user_agent)

        async with self.prepare():
            await self._check_super_user(admin_id=jwt_payload.user)

            limit_offset = entry_dto.get_limit_offset()
            count_res = await self.user_manager.get_rows_count()
            user_list = await self.user_manager.get_multi(limit=limit_offset.limit, offset=limit_offset.offset)
            if not user_list:
                raise UserListPageNotFoundError()

        return GetUserListResultDto(
            results=[
                UserInList(
                    id=user.id,
                    email=user.email,
                    is_active=user.is_active,
                    is_superuser=user.is_superuser,
                )
                for user in user_list
            ],
            **BasePaginationResultDto.create(
                total_count=count_res, page_number=entry_dto.page_number, page_size=entry_dto.page_size
            ),
        )

    async def create_policy(self, entry_dto: CreatePolicyEntryDto) -> CreatePolicyResultDto:
        jwt_payload = await self.process_access_jwt(token=entry_dto.access_token, user_agent=entry_dto.user_agent)

        async with self.prepare():
            await self._check_super_user(admin_id=jwt_payload.user)

            try:
                policy = Policy(**entry_dto.policy)
            except ValidationError as e:
                logger.exception(e)
                raise PolicyBadFormattedError()

            try:
                policy_model = await self.abac_pip_manager.create(obj_in=PolicyModelSchema(**policy.dict()))
            except IntegrityError:
                raise PolicyAlreadyExistsError()

        return CreatePolicyResultDto(id=policy_model.id)

    async def update_policy(self, entry_dto: UpdatePolicyEntryDto) -> UpdatePolicyResultDto:
        jwt_payload = await self.process_access_jwt(token=entry_dto.access_token, user_agent=entry_dto.user_agent)

        async with self.prepare():
            await self._check_super_user(admin_id=jwt_payload.user)

            try:
                policy = Policy(**entry_dto.policy)
            except ValidationError as e:
                logger.exception(e)
                raise PolicyBadFormattedError()

            policy_model = await self.abac_pip_manager.get(uuid=str(entry_dto.id))

            if not policy_model:
                raise PolicyNotFoundError()

            try:
                await self.abac_pip_manager.update(db_obj=policy_model, obj_in=PolicyModelSchema(**policy.dict()))
            except IntegrityError as e:
                logger.exception(e)
                raise PolicyAlreadyExistsError()

        return UpdatePolicyResultDto()

    async def delete_policy(self, entry_dto: DeletePolicyEntryDto) -> DeletePolicyResultDto:
        jwt_payload = await self.process_access_jwt(token=entry_dto.access_token, user_agent=entry_dto.user_agent)

        async with self.prepare():
            await self._check_super_user(admin_id=jwt_payload.user)

            policy_model = await self.abac_pip_manager.get(uuid=str(entry_dto.id))

            if not policy_model:
                raise PolicyNotFoundError()

            await self.abac_pip_manager.delete(db_obj=policy_model)

        return DeletePolicyResultDto()

    async def get_policy(self, entry_dto: GetPolicyEntryDto) -> GetPolicyResultDto:
        jwt_payload = await self.process_access_jwt(token=entry_dto.access_token, user_agent=entry_dto.user_agent)

        async with self.prepare():
            await self._check_super_user(admin_id=jwt_payload.user)
            policy_model = await self.abac_pip_manager.get(uuid=str(entry_dto.id))

            if not policy_model:
                raise PolicyNotFoundError()

        return GetPolicyResultDto(policy=self.abac_pip_manager.to_policy(policy_model).json())

    async def get_policy_list(self, entry_dto: GetPolicyListEntryDto) -> GetPolicyListResultDto:
        jwt_payload = await self.process_access_jwt(token=entry_dto.access_token, user_agent=entry_dto.user_agent)

        async with self.prepare():
            await self._check_super_user(admin_id=jwt_payload.user)
            limit_offset = entry_dto.get_limit_offset()

            count_res = await self.abac_pip_manager.get_rows_count()
            policy_models = await self.abac_pip_manager.get_multi(limit=limit_offset.limit, offset=limit_offset.offset)
            if not policy_models:
                raise PolicyListPageNotFoundError()

        return GetPolicyListResultDto(
            policy=[self.abac_pip_manager.to_policy(policy).json() for policy in policy_models],
            **BasePaginationResultDto.create(
                total_count=count_res, page_number=entry_dto.page_number, page_size=entry_dto.page_size
            ),
        )

    async def _get_subject(self, user_id: str) -> UserSubject:
        if not user_id:
            return UserSubject(is_user=False, is_superuser=False)

        user = await self.user_manager.get(uuid=user_id)
        if not user or not user.is_active:
            return UserSubject(is_user=False, is_superuser=False)

        if not user.is_superuser:
            return UserSubject(is_user=True, is_superuser=False)

        return UserSubject(is_user=True, is_superuser=True)

    @BaseService.cache(model_type=CheckAccessResultDto, ttl=30)
    async def _check_access(
        self, user_id: str, resource: dict[str, Any] | str, action: dict[str, Any] | str, context: dict[str, Any] | str
    ) -> CheckAccessResultDto:
        async with self.prepare():
            subject = await self._get_subject(user_id=user_id)

            if subject.is_superuser:
                has_access = True
            else:
                inquiry = Inquiry(
                    resource=resource,
                    action=action,
                    subject={
                        Constants.SUBJECT_IS_USER: subject.is_user,
                        Constants.SUBJECT_IS_SUPERUSER: subject.is_superuser,
                    },
                    context=context,
                )

                has_access = await self.abac_pdp_manager.is_allowed(inquiry=inquiry)

        return CheckAccessResultDto(has_access=has_access)

    async def check_access(self, entry_dto: CheckAccessEntryDto) -> CheckAccessResultDto:
        user_id = ""
        resource = entry_dto.inquiry.get(Constants.RESOURCE, "")
        action = entry_dto.inquiry.get(Constants.ACTION, "")
        context = {Constants.CONTEXT_USER_AGENT: entry_dto.user_agent, Constants.CONTEXT_IP_ADDRESS: entry_dto.ip}

        if entry_dto.access_token:
            try:
                jwt_payload = await self.process_access_jwt(
                    token=entry_dto.access_token, user_agent=entry_dto.user_agent
                )
                user_id = jwt_payload.user
            except BaseTokenError:
                user_id = ""

        return await self._check_access(user_id=user_id, resource=resource, action=action, context=context)
