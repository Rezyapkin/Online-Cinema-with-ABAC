from enum import Enum

from fastapi import HTTPException, status


class Exceptions(str, Enum):
    FILMS_NOT_FOUND = "Films not found."
    FILM_NOT_FOUND = "Film not found."
    GENRES_NOT_FOUND = "Genres not found"
    GENRE_NOT_FOUND = "Genre not found"
    PERSONS_NOT_FOUND = "Persons not found"
    PERSON_NOT_FOUND = "Person not found"
    PERSON_FILMS_NOT_FOUND = "Films for person not found."


def raise_not_found(message: Exceptions):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
