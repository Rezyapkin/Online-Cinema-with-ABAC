from fastapi import APIRouter, status

from . import film as film_route, genre as genre_route, person as person_route

router = APIRouter(responses={status.HTTP_404_NOT_FOUND: {"description": "Page not found"}})

router.include_router(film_route.router, prefix="/films", tags=["Films"])
router.include_router(genre_route.router, prefix="/genres", tags=["Genres"])
router.include_router(person_route.router, prefix="/persons", tags=["Persons"])
