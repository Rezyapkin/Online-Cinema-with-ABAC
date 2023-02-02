from uuid import UUID

from fastapi import APIRouter, Depends, Query

from services.film import FilmService, get_film_service
from .dependencies import get_paginator, Paginator, Searcher, get_film_filters, get_searcher, FilmListFilter
from .exceptions import raise_not_found, Exceptions
from .schemas.film import BaseFilm, Film, FilmListSorting, FilmListWithPagination

router = APIRouter()


def process_films_with_pagination(films_response) -> FilmListWithPagination:
    if not films_response:
        raise_not_found(Exceptions.FILMS_NOT_FOUND)

    return FilmListWithPagination(
        count=films_response.count,
        total_pages=films_response.total_pages,
        prev=films_response.prev,
        next=films_response.next,
        results=[
            BaseFilm(
                uuid=film.uuid,
                title=film.title,
                imdb_rating=film.imdb_rating,
                release_date=film.release_date,
                age_limit=film.age_limit,
            )
            for film in films_response.results
        ],
    )


@router.get(
    "/search",
    response_model=FilmListWithPagination,
    summary="Поиск по фильмам",
    description="Поиск фильмов",
    response_description="Список кинопроизведений и их рейтинг",
    tags=["Films"],
)
async def films_search(
    paginator: Paginator = Depends(get_paginator),
    search: Searcher = Depends(get_searcher),
    film_service: FilmService = Depends(get_film_service),
) -> FilmListWithPagination:
    films_response = await film_service.search_films(
        search_query=search.query,
        page_size=paginator.size,
        page_num=paginator.page,
    )

    return process_films_with_pagination(films_response)


@router.get(
    "/{film_id}/",
    response_model=Film,
    response_model_by_alias=False,
    summary="Поиск кинопроизведений",
    description="Поиск кинопроизведения по uuid",
    response_description="Детальная информация по кинопроизведению",
    tags=["Films"],
)
async def film_details(
    film_id: UUID,
    film_service: FilmService = Depends(get_film_service),
) -> Film:
    film = await film_service.get_film(film_id=film_id)

    if not film:
        raise_not_found(Exceptions.FILM_NOT_FOUND)

    return Film(
        uuid=film.uuid,
        title=film.title,
        imdb_rating=film.imdb_rating,
        release_date=film.release_date,
        age_limit=film.age_limit,
        description=film.description,
        genres=film.genres,
        actors=film.actors,
        writers=film.writers,
        directors=film.directors,
    )


@router.get(
    "/",
    response_model=FilmListWithPagination,
    summary="Перечень кинопроизведений",
    description="Перечень кинопроизведений с сортировкой и фильтрацией",
    response_description="Список кинопроизведений и их рейтинг",
    tags=["Films"],
)
async def films_list(
    paginator: Paginator = Depends(get_paginator),
    filters: FilmListFilter = Depends(get_film_filters),
    sort: FilmListSorting | None = Query(default=None),
    film_service: FilmService = Depends(get_film_service),
) -> FilmListWithPagination:
    films_response = await film_service.get_films(
        filters=filters,
        sort=sort,
        page_size=paginator.size,
        page_num=paginator.page,
    )

    return process_films_with_pagination(films_response)
