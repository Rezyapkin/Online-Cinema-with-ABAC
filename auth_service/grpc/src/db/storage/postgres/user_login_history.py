from sqlalchemy import select, desc, update, func
from user_agents import parse

from core.tracer import instrumented
from db.storage import BaseAsyncCrudStorage
from models.postgres.user_login_history import UserLoginHistory, DeviceEnum, UserLoginHistorySchema


class UserLoginHistoryCrudStorage(BaseAsyncCrudStorage[UserLoginHistorySchema, UserLoginHistory]):
    model: type[UserLoginHistory] = UserLoginHistory

    @staticmethod
    def get_device(user_agent: str) -> DeviceEnum:
        parsed_ua = parse(user_agent)
        if "smart" in user_agent.lower():
            device = DeviceEnum.smart_tv
        elif parsed_ua.is_mobile:
            device = DeviceEnum.mobile
        else:
            device = DeviceEnum.web

        return device

    @instrumented
    async def create(self, *, obj_in: UserLoginHistorySchema) -> UserLoginHistory:
        obj_in.device = self.get_device(obj_in.user_agent)
        return await super().create(obj_in=obj_in)

    @instrumented
    async def get_login_history(self, user_id: str, limit: int, offset: int) -> list[UserLoginHistory] | None:
        statement = (
            select(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(desc(self.model.created_at))
            .offset(offset)
            .limit(limit)
        )
        results = await self._storage.execute(statement=statement)
        return results.scalars().all()

    @instrumented
    async def get_count_by_user(self, user_id: str) -> int:
        query = (
            select([self.model.user_id, func.count(self.model.user_id)])
            .group_by(self.model.user_id)
            .filter(self.model.user_id == user_id)
        )
        result = await self._storage.execute(query)
        if cnt := result.fetchone():
            return cnt[1]

        return 0

    @instrumented
    async def activate_latest_session(self, user_id: str, user_agent: str) -> None:
        statement = (
            select(self.model)
            .filter(self.model.user_id == user_id, self.model.user_agent == user_agent)
            .order_by(desc(self.model.created_at))
            .limit(1)
        )
        result = await self._storage.execute(statement=statement)

        await self.update(db_obj=result.scalar_one_or_none(), obj_in={"is_active": True})

    @instrumented
    async def disable_user_sessions(self, user_id: str) -> None:
        statement = update(self.model).filter(self.model.user_id == user_id).values({self.model.is_active: False})
        await self._storage.execute(statement=statement)
        await self._storage.commit()
