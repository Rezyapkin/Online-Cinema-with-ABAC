import bcrypt
from uuid import uuid4

from core.tracer import instrumented
from db.storage.base import BaseAsyncCrudStorage
from models.postgres.user import User, UserSchema


class UserCrudStorage(BaseAsyncCrudStorage[UserSchema, User]):
    model: type[User] = User

    @staticmethod
    @instrumented
    def is_valid_password(user: User, password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=user.hashed_password.encode(),
        )

    @instrumented
    async def create(self, *, obj_in: UserSchema) -> User:
        obj_in.hashed_password = bcrypt.hashpw(
            password=obj_in.hashed_password.encode(),
            salt=bcrypt.gensalt(),
        ).decode("utf-8")
        return await super().create(obj_in=obj_in)

    @instrumented
    async def get_or_create_by_email(self, email: str) -> User:
        user = await self.get_first_by(email=email)

        if user:
            return user

        return await self.create(obj_in=UserSchema(email=email, hashed_password=str(uuid4())))

    @instrumented
    async def update(self, db_obj: User, *, obj_in: UserSchema | dict) -> User:
        if obj_in.get("hashed_password"):
            obj_in["hashed_password"] = bcrypt.hashpw(
                password=obj_in["hashed_password"].encode(),
                salt=bcrypt.gensalt(),
            ).decode("utf-8")

        return await super().update(db_obj=db_obj, obj_in=obj_in)
