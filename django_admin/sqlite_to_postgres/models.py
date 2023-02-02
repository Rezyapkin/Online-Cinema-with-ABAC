from dataclasses import dataclass


@dataclass
class IDMixin:
    id: str


@dataclass
class TimeStampedMixin:
    created_at: str
    updated_at: str


@dataclass
class Filmwork(IDMixin, TimeStampedMixin):
    table_name = "film_work"

    title: str
    type: str
    description: str | None = None
    creation_date: str | None = None
    rating: float | None = None
    file_path: str | None = None
    certificate: str | None = None


@dataclass
class Genre(IDMixin, TimeStampedMixin):
    table_name = "genre"

    name: str
    description: str | None = None


@dataclass
class Person(IDMixin, TimeStampedMixin):
    table_name = "person"

    full_name: str


@dataclass
class GenreFilmwork(IDMixin):
    table_name = "genre_film_work"

    genre_id: str
    film_work_id: str
    created_at: str


@dataclass
class PersonFilmwork(IDMixin):
    table_name = "person_film_work"

    person_id: str
    film_work_id: str
    created_at: str
    role: str | None = None
