from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Iterable, Generic, TypeVar

from pydantic import BaseModel, Field, root_validator

from core.helpers.decorators import chain
from core.tracer import instrumented

IndexModelType = TypeVar("IndexModelType", bound=BaseModel)


class EntitiesAndCountModel(BaseModel, Generic[IndexModelType]):
    count: int
    entities: list[IndexModelType]


class ComparisonOperators(str, Enum):
    EQ = "equality"
    IN = "in"
    RANGE = "range"


class FilterEntity(BaseModel):
    field_name: str
    comparison_operator: ComparisonOperators = ComparisonOperators.EQ
    value: Any

    @root_validator()
    def validate_consistency_comparison_operator_with_value(cls, values):  # noqa: N805
        if values["comparison_operator"] == ComparisonOperators.IN:
            if not isinstance(values["value"], Iterable):
                raise AssertionError("For the `IN` operator, the value field must be an iterable object")
        elif values["comparison_operator"] == ComparisonOperators.RANGE:
            if not isinstance(values["value"], Iterable) or len(values["value"]) != 2:
                raise AssertionError("For the `RANGE` operator, the value field must be an iterable object of length 2")
        return values


class LogicalGroupOperators(str, Enum):
    AND = "and"
    OR = "or"


class FilterGroup(BaseModel):
    logical_group_operator: LogicalGroupOperators
    entities: list["FilterEntity | FilterGroup"]


FilterGroup.update_forward_refs()


class SortingOrders(str, Enum):
    ASC = "asc"
    DESC = "desc"


class SortEntity(BaseModel):
    field_name: str
    order: SortingOrders = SortingOrders.ASC


class SearchTypes(str, Enum):
    FUZZY = "fuzzy search"
    CLEAR = "clear search"


class SearchString(BaseModel):
    search_string: str = Field(min_length=1)
    search_fields: list[str]
    type_search: SearchTypes


class QueryBuilder(Generic[IndexModelType]):
    """A class for building queries to get data from storage."""

    filter_: FilterGroup | FilterEntity | None = None
    sorts_: list[SortEntity] | None = None
    search_query_: SearchString | None = None
    offset_: int = 0

    def __init__(self, storage: "BaseStorage[IndexModelType]"):
        self.storage = storage

    @chain
    def filter(
        self,
        filter_entity: FilterGroup | FilterEntity,
        group_operator: LogicalGroupOperators = LogicalGroupOperators.AND,
    ):
        if self.filter_ is None:
            self.filter_ = filter_entity
        elif (
            isinstance(self.filter_, FilterGroup)
            and isinstance(filter_entity, FilterEntity)
            and self.filter_.logical_group_operator == group_operator
        ):
            self.filter_.entities.append(filter_entity)
        else:
            self.filter_ = FilterGroup(logical_group_operator=group_operator, entities=[self.filter, filter_entity])

    @chain
    def sort(self, *sorts: SortEntity):
        if self.sorts_ is None:
            self.sorts_ = []
        self.sorts_.extend(sorts)

    @chain
    def search(self, search_query: SearchString):
        self.search_query_ = search_query

    @chain
    def offset(self, offset: int):
        self.offset_ = offset

    @instrumented
    async def fetch(self, batch_size: int = 50) -> list[IndexModelType]:
        """Calls the method of the same name from the storage class."""
        return await self.storage.fetch(self, batch_size)

    @instrumented
    async def fetch_count(self, batch_size: int = 50) -> EntitiesAndCountModel[IndexModelType]:
        """Calls the method of the same name from the storage class."""
        return await self.storage.fetch_count(self, batch_size)


class AbstractBaseStorage(ABC):
    def __init__(self, client: any):
        self._storage: any = client

    @abstractmethod
    async def ping(self) -> bool:
        """
        An abstract method to check the storage state
        """
        raise NotImplementedError

    async def close_storage(self):
        await self._storage.close()


class BaseStorage(AbstractBaseStorage, Generic[IndexModelType]):
    model_type: type[IndexModelType]

    @abstractmethod
    async def get_entity(self, key: str) -> IndexModelType:
        raise NotImplementedError

    @abstractmethod
    async def fetch(
        self, query: QueryBuilder[IndexModelType] | None = None, batch_size: int = 50
    ) -> list[IndexModelType] | None:
        raise NotImplementedError

    @abstractmethod
    async def fetch_count(
        self, query: QueryBuilder[IndexModelType] | None = None, batch_size: int = 50
    ) -> EntitiesAndCountModel[IndexModelType] | None:
        raise NotImplementedError

    def query(self) -> QueryBuilder[IndexModelType]:
        return QueryBuilder(self)
