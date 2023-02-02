from uuid import UUID

from fastapi import APIRouter, Depends

from services.film import FilmService, get_film_service
from services.person import get_person_service, PersonService
from .dependencies import get_searcher, Searcher, Paginator, get_paginator
from .exceptions import raise_not_found, Exceptions
from .schemas.film import BaseFilm
from .schemas.person import Person, PersonListWithPagination

router = APIRouter()


@router.get(
    "/search",
    response_model=PersonListWithPagination,
    summary="Поиск по персонам",
    description="Поиск информации по персонам",
    response_description="Список персон, сотответствующий параметрам поиска",
    tags=["Persons"],
)
async def persons_search(
    searcher: Searcher = Depends(get_searcher),
    paginator: Paginator = Depends(get_paginator),
    service: PersonService = Depends(get_person_service),
) -> PersonListWithPagination:
    persons_response = await service.search_persons(
        search_query=searcher.query,
        page_size=paginator.size,
        page_num=paginator.page,
    )

    if not persons_response:
        raise_not_found(Exceptions.PERSONS_NOT_FOUND)

    return PersonListWithPagination(
        count=persons_response.count,
        total_pages=persons_response.total_pages,
        prev=persons_response.prev,
        next=persons_response.next,
        results=[
            Person(
                uuid=person.uuid,
                full_name=person.full_name,
                role=person.role,
                films=person.films,
            )
            for person in persons_response.results
        ],
    )


@router.get(
    "/{person_id}/film",
    response_model=list[BaseFilm],
    summary="Фильмы по персоне",
    description="Список фильмов с участием персоны",
    response_description="Список фильмов",
    tags=["Persons"],
)
async def person_films(
    person_id: UUID,
    service: FilmService = Depends(get_film_service),
) -> list[BaseFilm]:
    films = await service.get_person_films(person_id=person_id)

    if not films:
        raise_not_found(Exceptions.PERSON_FILMS_NOT_FOUND)

    return [
        BaseFilm(
            uuid=film.uuid,
            title=film.title,
            imdb_rating=film.imdb_rating,
            release_date=film.release_date,
            age_limit=film.age_limit,
        )
        for film in films
    ]


@router.get(
    "/{person_id}/",
    response_model=Person,
    summary="Данные о персоне",
    description="Информация о персоне по ее UUID",
    response_description="Данные персоны",
    tags=["Persons"],
)
async def person_details(
    person_id: UUID,
    service: PersonService = Depends(get_person_service),
) -> Person:
    person = await service.get_person(person_id=person_id)

    if not person:
        raise_not_found(Exceptions.PERSON_NOT_FOUND)

    return Person(
        uuid=person.uuid,
        full_name=person.full_name,
        role=person.role,
        films=person.films,
    )
