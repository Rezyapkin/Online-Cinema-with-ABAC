from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.storage.elasticsearch import get_elastic
from db.storage.elasticsearch.base import BaseElasticStorage
from models.genre import Genre


class GenreElasticStorage(BaseElasticStorage[Genre]):
    index_name = "genres"
    model_type = Genre
    result_fields = None


@lru_cache
def get_genre_elastic_storage(client: AsyncElasticsearch = Depends(get_elastic)) -> GenreElasticStorage:
    return GenreElasticStorage(client)
