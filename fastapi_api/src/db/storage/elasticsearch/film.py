from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.storage.elasticsearch import get_elastic
from db.storage.elasticsearch.base import BaseElasticStorage
from models.film import Film


class FilmElasticStorage(BaseElasticStorage[Film]):
    index_name = "movies"
    model_type = Film
    result_fields = None


@lru_cache
def get_film_elastic_storage(client: AsyncElasticsearch = Depends(get_elastic)) -> FilmElasticStorage:
    return FilmElasticStorage(client)
