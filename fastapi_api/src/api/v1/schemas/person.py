from enum import Enum

from pydantic import Field

from .results import PaginateResultsModel
from .uuid_mixin import UUIDMixin


class PersonRoles(str, Enum):
    ACTOR = "actor"
    DIRECTOR = "director"
    PRODUCER = "producer"
    WRITER = "writer"


class BasePerson(UUIDMixin):
    full_name: str = Field(description="Имя, фамилия")

    class Config:
        schema_extra = {
            "example": {
                "uuid": "524e4331-e14b-24d3-a456-426614174002",
                "full_name": "George Lucas",
            }
        }


class FilmInfoByPerson(UUIDMixin):
    title: str = Field(description="Название фильма")


class Person(BasePerson):
    role: list[PersonRoles] | None = Field(description="Роль участия в фильме")
    films: list[FilmInfoByPerson] | None = Field(description="Все фильмы, в которых принимал участие")

    class Config:
        schema_extra = {
            "example": {
                "uuid": "524e4331-e14b-24d3-a456-426614174002",
                "full_name": "George Lucas",
                "role": ["writer", "director"],
                "films": [
                    {
                        "uuid": "223e4317-e89b-22d3-f3b6-426614174000",
                        "title": "Billion Star Hotel",
                    }
                ],
            }
        }


class PersonListWithPagination(PaginateResultsModel[Person]):
    results: list[Person] = Field(description="Список персон")

    class Config:
        schema_extra = {
            "example": {
                "count": 100,
                "total_pages": 10,
                "next_page": 2,
                "prev_page": None,
                "results": [
                    {
                        "uuid": "524e4331-e14b-24d3-a456-426614174002",
                        "full_name": "George Lucas",
                        "role": ["writer", "director"],
                        "films": [
                            {
                                "uuid": "223e4317-e89b-22d3-f3b6-426614174000",
                                "title": "Billion Star Hotel",
                            },
                            {
                                "uuid": "118fd71b-93cd-4de5-95a4-e1485edad30e",
                                "title": "Rogue One: A Star Wars Story",
                            },
                        ],
                    }
                ],
            }
        }
