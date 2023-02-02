from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.storage.elasticsearch import get_elastic
from db.storage.elasticsearch.base import BaseElasticStorage
from models.person import BasePerson


class PersonElasticStorage(BaseElasticStorage[BasePerson]):
    index_name = "persons"
    model_type = BasePerson
    result_fields = None


@lru_cache
def get_person_elastic_storage(client: AsyncElasticsearch = Depends(get_elastic)) -> PersonElasticStorage:
    return PersonElasticStorage(client)
