from sqlalchemy import select, asc

from db.storage.base import BaseAsyncCrudStorage
from models.postgres.oauth import UserOAuthAccount, UserOAuthAccountSchema


class UserOAuthAccountCrudStorage(BaseAsyncCrudStorage[UserOAuthAccountSchema, UserOAuthAccount]):
    model: type[UserOAuthAccount] = UserOAuthAccount

    async def get_user_oauth_accounts(self, user_id: str) -> list[UserOAuthAccount] | None:
        statement = (
            select(self.model).filter(self.model.user_id == user_id).order_by(asc(self.model.oauth_provider_name))
        )
        results = await self._storage.execute(statement=statement)
        return results.scalars().all()
