from uuid import UUID

from fastapi import Query
from pydantic import BaseModel


class Paginator(BaseModel):
    page: int
    size: int


class Searcher(BaseModel):
    query: str


class FilmListFilter(BaseModel):
    genre: UUID | None


async def get_paginator(
    page: int = Query(default=1, alias="page[number]", description="Номер страницы", ge=1, le=50),
    size: int = Query(default=10, alias="page[size]", description="Размер страницы", ge=1, le=100),
) -> Paginator:
    return Paginator(page=page, size=size)


async def get_searcher(query: str = Query(description="Строка поиска", min_length=1)) -> Searcher:
    return Searcher(query=query)


async def get_film_filters(
    genre: UUID | None = Query(default=None, alias="filter[genre]", description="UUID жанра"),
) -> FilmListFilter:
    return FilmListFilter(genre=genre)
