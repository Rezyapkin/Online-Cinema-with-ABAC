from abc import ABC
from datetime import datetime
from typing import TypeVar

from _socket import gaierror
from sqlalchemy import select, desc, func
from sqlalchemy.exc import InterfaceError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import expression

from core.tracer import instrumented
from db.base import AbstractAsyncCrudStorage
from models.postgres import Base, SchemaInDbType

CrudModelType = TypeVar("CrudModelType", bound=Base)


class BaseAsyncCrudStorage(AbstractAsyncCrudStorage[SchemaInDbType, CrudModelType], ABC):
    model: type[CrudModelType]

    def __init__(self, client: AsyncSession):
        self._storage: AsyncSession
        super().__init__(client)

    @instrumented
    async def execute(self, statement: expression) -> list[CrudModelType]:
        results = await self._storage.execute(statement=statement)
        return results.scalars().all()

    async def _ping(self) -> bool:
        try:
            await self._storage.execute(statement="SELECT 1")
        except (gaierror, InterfaceError):
            return False

        return True

    @instrumented
    async def get(self, uuid: str) -> CrudModelType | None:
        statement = select(self.model).where(self.model.id == uuid)
        results = await self._storage.execute(statement=statement)
        return results.scalar_one_or_none()

    @instrumented
    async def get_first_by(self, order_by_creation: bool = False, **kwargs) -> CrudModelType | None:
        statement = select(self.model).filter_by(**kwargs)

        if order_by_creation:
            statement = statement.order_by(desc(self.model.created_at))

        results = await self._storage.execute(statement=statement)
        return results.scalars().first()

    @instrumented
    async def get_multi(self, *, offset: int = 0, limit: int = 100) -> list[CrudModelType] | None:
        statement = select(self.model).offset(offset).limit(limit)
        results = await self._storage.execute(statement=statement)
        return results.scalars().all()

    @instrumented
    async def get_rows_count(self) -> int:
        statement = select([func.count()]).select_from(self.model)
        result = await self._storage.execute(statement=statement)
        return result.scalar()

    @instrumented
    async def update(self, db_obj: CrudModelType, *, obj_in: SchemaInDbType | dict) -> CrudModelType:
        for key, value in dict(obj_in).items():
            setattr(db_obj, key, value)

        if hasattr(db_obj, "updated_at"):
            db_obj.updated_at = datetime.utcnow()

        await self._storage.commit()
        await self._storage.refresh(db_obj)
        return db_obj

    @instrumented
    async def create(self, *, obj_in: SchemaInDbType) -> CrudModelType:
        db_obj = self.model(**obj_in.dict())
        self._storage.add(db_obj)
        await self._storage.commit()
        await self._storage.refresh(db_obj)
        return db_obj

    @instrumented
    async def delete(self, *, db_obj: CrudModelType) -> None:
        await self._storage.delete(db_obj)
        await self._storage.commit()
