from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import AsyncGenerator

from core.tracer import instrumented
from db.storage.base import BaseAsyncCrudStorage
from models.postgres.abac import (
    PolicyModel,
    PolicyModelSchema,
    PolicySubjectModel,
    PolicyResourceModel,
    PolicyActionModel,
)
from services.abac.effects import Effects
from services.abac.policy import Policy


class ABACCrudStorage(BaseAsyncCrudStorage[PolicyModelSchema, PolicyModel]):
    model: type[PolicyModel] = PolicyModel

    @instrumented
    async def create(self, *, obj_in: PolicyModelSchema) -> PolicyModel:
        db_obj = self.model(
            description=obj_in.description,
            effect=obj_in.effect,
            context=obj_in.context,
            subjects=[PolicySubjectModel(subject=x) for x in obj_in.subjects],
            resources=[PolicyResourceModel(resource=x) for x in obj_in.resources],
            actions=[PolicyActionModel(action=x) for x in obj_in.actions],
        )
        self._storage.add(db_obj)
        await self._storage.commit()
        await self._storage.refresh(db_obj)
        return db_obj

    @instrumented
    async def update(self, db_obj: PolicyModel, *, obj_in: PolicyModelSchema | dict) -> PolicyModel:
        # reset all 1-to-many realationship (mvp api)
        await self._storage.execute(
            statement=delete(PolicySubjectModel).where(PolicySubjectModel.policy_id == db_obj.id)
        )
        await self._storage.execute(
            statement=delete(PolicyResourceModel).where(PolicyResourceModel.policy_id == db_obj.id)
        )
        await self._storage.execute(statement=delete(PolicyActionModel).where(PolicyActionModel.policy_id == db_obj.id))

        obj_in.subjects = [PolicySubjectModel(subject=x) for x in obj_in.subjects]
        obj_in.resources = [PolicyResourceModel(resource=x) for x in obj_in.resources]
        obj_in.actions = [PolicyActionModel(action=x) for x in obj_in.actions]

        for key, value in dict(obj_in).items():
            setattr(db_obj, key, value)

        db_obj.updated_at = datetime.utcnow()

        await self._storage.commit()
        await self._storage.refresh(db_obj)
        return db_obj

    @instrumented
    async def get(self, uuid: str) -> PolicyModel | None:
        statement = (
            select(self.model)
            .options(
                selectinload(self.model.subjects),
                selectinload(self.model.resources),
                selectinload(self.model.actions),
            )
            .where(self.model.id == uuid)
        )
        results = await self._storage.execute(statement=statement)
        return results.scalar_one_or_none()

    @instrumented
    async def get_multi(self, *, offset=0, limit=100) -> list[PolicyModel] | None:
        statement = (
            select(self.model)
            .options(
                selectinload(self.model.subjects),
                selectinload(self.model.resources),
                selectinload(self.model.actions),
            )
            .offset(offset)
            .limit(limit)
        )
        results = await self._storage.execute(statement=statement)
        return results.scalars().all()

    @staticmethod
    def to_policy(db_obj: PolicyModel) -> Policy:
        return Policy(
            id=db_obj.id,
            effect=Effects.ALLOW_ACCESS if db_obj.effect else Effects.DENY_ACCESS,
            description=db_obj.description,
            context=db_obj.context,
            subjects=[x.subject for x in db_obj.subjects],
            resources=[x.resource for x in db_obj.resources],
            actions=[x.action for x in db_obj.actions],
        )

    async def find_for_inquiry(self) -> AsyncGenerator[Policy, None]:
        policies = await self.get_multi()
        for policy_model in policies:
            yield self.to_policy(db_obj=policy_model)
