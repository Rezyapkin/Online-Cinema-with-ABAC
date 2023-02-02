from pydantic import Field

from .results import PaginateResultsModel
from .uuid_mixin import UUIDMixin


class Genre(UUIDMixin):
    name: str = Field(description="Название жанра")

    class Config:
        schema_extra = {
            "example": {
                "uuid": "524e4331-e14b-24d3-a456-426614174001",
                "name": "Action",
            }
        }


class GenreListWithPagination(PaginateResultsModel[Genre]):
    results: list[Genre] = Field(description="Список жанров")

    class Config:
        schema_extra = {
            "example": {
                "count": 20,
                "total_pages": 10,
                "next_page": 2,
                "prev_page": None,
                "results": [
                    {
                        "uuid": "524e4331-e14b-24d3-a456-426614174001",
                        "name": "Action",
                    },
                    {
                        "uuid": "120a21cf-9097-479e-904a-13dd7198c1dd",
                        "name": "Adventure",
                    },
                    {
                        "uuid": "b92ef010-5e4c-4fd0-99d6-41b6456272cd",
                        "name": "Fantasy",
                    },
                ],
            }
        }
