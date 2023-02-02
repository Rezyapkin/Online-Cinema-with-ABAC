from uuid import UUID

from fastapi import APIRouter, Depends

from services.genre import GenreService, get_genre_service
from .dependencies import Paginator, get_paginator
from .exceptions import raise_not_found, Exceptions
from .schemas.genre import Genre, GenreListWithPagination

router = APIRouter()


@router.get(
    "/{genre_id}/",
    response_model=Genre,
    summary="Данные по жанру",
    description="Информация о жанре по его UUID",
    response_description="Данные жанра",
    tags=["Genres"],
)
async def genre_details(
    genre_id: UUID,
    service: GenreService = Depends(get_genre_service),
) -> Genre:
    genre = await service.get_genre(genre_id=genre_id)

    if not genre:
        raise raise_not_found(Exceptions.GENRE_NOT_FOUND)

    return Genre(
        uuid=genre.uuid,
        name=genre.name,
    )


@router.get(
    "/",
    response_model=GenreListWithPagination,
    summary="Список жанров",
    description="Список всех жанров",
    response_description="Список жанров",
    tags=["Genres"],
)
async def genres_list(
    service: GenreService = Depends(get_genre_service),
    paginator: Paginator = Depends(get_paginator),
) -> GenreListWithPagination:
    genres_response = await service.get_genres(
        page_size=paginator.size,
        page_num=paginator.page,
    )

    if not genres_response:
        raise_not_found(Exceptions.GENRES_NOT_FOUND)

    return GenreListWithPagination(
        count=genres_response.count,
        total_pages=genres_response.total_pages,
        prev=genres_response.prev,
        next=genres_response.next,
        results=[
            Genre(
                uuid=genre.uuid,
                name=genre.name,
            )
            for genre in genres_response.results
        ],
    )
