from datetime import date
from enum import Enum

from pydantic import Field

from .genre import Genre
from .person import BasePerson
from .results import PaginateResultsModel
from .uuid_mixin import UUIDMixin


class FilmListSorting(str, Enum):
    RATING_ASC = "imdb_rating"
    RATING_DESC = "-imdb_rating"


class FilmAgeLimit(str, Enum):
    G = "General Audiences"
    PG = "Parental Guidance Suggested"
    PG_13 = "Parents Strongly Cautioned"
    R = "Restricted"
    NC_17 = "Adults Only"


class BaseFilm(UUIDMixin):
    title: str = Field(description="Название фильма")
    imdb_rating: float | None = Field(description="Рейтинг фильма от 0 до 10")
    release_date: date | None
    age_limit: FilmAgeLimit | None

    class Config:
        schema_extra = {
            "example": {
                "uuid": "223e4317-e89b-22d3-f3b6-426614174000",
                "title": "Billion Star Hotel",
                "imdb_rating": 6.1,
                "release_date": "2008-09-15",
                "age_limit": "General Audiences",
            }
        }


class Film(BaseFilm):
    description: str | None = Field(description="Описание фильма")
    genres: list[Genre] | None = Field(description="Список жанров")
    actors: list[BasePerson] | None = Field(description="Список актеров")
    writers: list[BasePerson] | None = Field(description="Список авторов фильма")
    directors: list[BasePerson] | None = Field(description="Список режисеров")

    class Config:
        schema_extra = {
            "example": {
                "uuid": "b31592e5-673d-46dc-a561-9446438aea0f",
                "title": "Lunar: The Silver Star",
                "imdb_rating": 9.2,
                "release_date": "2008-09-15",
                "age_limit": "General Audiences",
                "description": "From the village of Burg, a teenager named Alex sets out to become the fabled...",
                "genres": [
                    {"uuid": "6f822a92-7b51-4753-8d00-ecfedf98a937", "name": "Action"},
                    {"uuid": "00f74939-18b1-42e4-b541-b52f667d50d9", "name": "Adventure"},
                    {"uuid": "7ac3cb3b-972d-4004-9e42-ff147ede7463", "name": "Comedy"},
                ],
                "actors": [
                    {"uuid": "afbdbaca-04e2-44ca-8bef-da1ae4d84cdf", "full_name": "Ashley Parker Angel"},
                    {"uuid": "3c08931f-6138-46d1-b179-1bd076b6a236", "full_name": "Rhonda Gibson"},
                ],
                "writers": [
                    {"uuid": "1bd9a00b-9596-49a3-afbe-f39a632a09a9", "full_name": "Toshio Akashi"},
                    {"uuid": "27fc3dc6-2656-43cb-8e56-d0dfb75ea0b2", "full_name": "Takashi Hino"},
                ],
                "directors": [{"uuid": "4a893a97-e713-4936-9dd4-c8ca437ab483", "full_name": "Toshio Akashi"}],
            }
        }


class FilmListWithPagination(PaginateResultsModel[BaseFilm]):
    results: list[BaseFilm] = Field(description="Список фильмов")

    class Config:
        schema_extra = {
            "example": {
                "count": 500,
                "total_pages": 10,
                "next_page": 2,
                "prev_page": None,
                "results": [
                    {
                        "uuid": "b31592e5-673d-46dc-a561-9446438aea0f",
                        "title": "Lunar: The Silver Star",
                        "imdb_rating": 9.2,
                        "release_date": "2008-09-15",
                        "age_limit": "General Audiences",
                    },
                    {
                        "uuid": "223e4317-e89b-22d3-f3b6-426614174000",
                        "title": "Billion Star Hotel",
                        "imdb_rating": 6.1,
                        "release_date": "2010-01-01",
                        "age_limit": "Adults Only",
                    },
                ],
            }
        }
