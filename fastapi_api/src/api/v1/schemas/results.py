from typing import Generic, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

ResultEntityModelType = TypeVar("ResultEntityModelType", bound=BaseModel)


class PaginateResultsModel(GenericModel, Generic[ResultEntityModelType]):
    count: int = Field(description="Общее количество записей")
    total_pages: int = Field(description="Общее количество страниц")
    prev: int | None = Field(description="Номер предыдущей страницы")
    next: int | None = Field(description="Номер следующей страницы")
    results: list[ResultEntityModelType]
