from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.tracer import instrumented
from db.storage.base import (
    BaseStorage,
    ComparisonOperators,
    EntitiesAndCountModel,
    FilterEntity,
    FilterGroup,
    LogicalGroupOperators,
    IndexModelType,
    QueryBuilder,
    SearchString,
    SearchTypes,
)
from db.storage.elasticsearch import get_elastic


class BaseElasticStorage(BaseStorage[IndexModelType]):
    index_name: str
    model_type: type[IndexModelType]
    result_fields: list[str] | None

    def __init__(self, client: AsyncElasticsearch):
        self._storage: AsyncElasticsearch
        super().__init__(client)

    async def ping(self) -> bool:
        return self._storage and await self._storage.ping()

    async def _get_entity(self, key: str) -> any:
        """Returns the raw-data from ElasticSearch by document `id`."""
        try:
            doc = await self._storage.get(index=self.index_name, id=key)
        except NotFoundError:
            return None

        return doc

    async def get_entity(self, key: str) -> IndexModelType | None:
        """Returns the Pydantic model from ElasticSearch by document `id`."""
        doc = await self._get_entity(key)

        if doc is None:
            return None

        return self.model_type(**doc["_source"])

    @staticmethod
    def get_elastic_filter_by_filter_entity(filter_entity: FilterEntity) -> dict[str, any]:
        """
        Converts filter entity to the format for passing the request body to ElasticSearch as a query parameter.

        `Example:`
            `FilterEntity(field_name='genres.id', value='00f74939-18b1-42e4-b541-b52f667d50d9')` convert to:
            `{'nested': {'path': 'genres', 'query': {'term': {'genres.id': '00f74939-18b1-42e4-b541-b52f667d50d9'}}}}`

        :param filter_entity: filter entity
        :return: query for ElasticSearch.
        """
        filter_query = {}
        current_filter = filter_query

        key_path_list = filter_entity.field_name.split(".")
        current_path = ""

        for index, key in enumerate(key_path_list):
            if current_path:
                current_path += f".{key}"
            else:
                current_path = key

            if index < len(key_path_list) - 1:
                new_depth_filter = {}
                current_filter["nested"] = {"path": current_path, "query": new_depth_filter}
                current_filter = new_depth_filter
            else:
                if filter_entity.comparison_operator == ComparisonOperators.IN:
                    current_filter["terms"] = {filter_entity.field_name: filter_entity.value}
                elif filter_entity.comparison_operator == ComparisonOperators.EQ:
                    current_filter["term"] = {filter_entity.field_name: filter_entity.value}
                elif filter_entity.comparison_operator == ComparisonOperators.RANGE:
                    current_filter["range"] = {
                        filter_entity.field_name: {
                            "gte": filter_entity.value[0],
                            "lte": filter_entity.value[1],
                        }
                    }

        return filter_query

    @classmethod
    def get_elastic_filter(cls, filter_: FilterEntity | FilterGroup | None) -> dict[str, any] | None:
        """
        Method that calls get_elastic_filter_by_filter_entity for FilterEntity and performs grouping for FilterGroup.
        """

        if filter_ is None:
            return None

        if isinstance(filter_, FilterEntity):
            return cls.get_elastic_filter_by_filter_entity(filter_)

        group_word = "must"
        if filter_.logical_group_operator == LogicalGroupOperators.OR:
            group_word = "should"

        filters = []
        filter_query = {"bool": {group_word: filters}}

        for filter_entity in filter_.entities:
            filters.append(cls.get_elastic_filter(filter_entity))

        return filter_query

    @staticmethod
    def get_elastic_query_by_search_string(search_string: SearchString | None) -> dict[str, any] | None:
        """Returns a dictionary for the ElasticSearch API to search by row in the repository."""

        if search_string is None:
            return None

        elastic_query = {
            "multi_match": {
                "query": search_string.search_string,
                "fields": search_string.search_fields,
            }
        }

        if search_string.type_search == SearchTypes.FUZZY:
            elastic_query["multi_match"]["fuzziness"] = "auto"

        return elastic_query

    async def _fetch(self, query: QueryBuilder | None, batch_size: int) -> dict[str, any]:
        if query is None:
            return await self._storage.search(index=self.index_name, filter_path=["hits.total", "hits.hits._source"])

        filter_query = self.get_elastic_filter(query.filter_)
        search_query = self.get_elastic_query_by_search_string(query.search_query_)

        elastic_query = filter_query
        if filter_query and search_query:
            elastic_query = {"bool": {"must": [search_query and filter_query]}}
        elif search_query:
            elastic_query = search_query

        return await self._storage.search(
            index=self.index_name,
            query=elastic_query,
            from_=query.offset_,
            size=batch_size,
            sort=[{sort.field_name: sort.order} for sort in query.sorts_] if query.sorts_ else None,
            filter_path=["hits.total", "hits.hits._source"],
            source=self.result_fields,
        )

    @instrumented
    async def fetch(self, query: QueryBuilder | None = None, batch_size: int = 50) -> list[IndexModelType] | None:
        docs = await self._fetch(query, batch_size)

        if documents := docs["hits"].get("hits", None):
            return [self.model_type(**value["_source"]) for value in documents]

    @instrumented
    async def fetch_count(
        self, query: QueryBuilder | None = None, batch_size: int = 50
    ) -> EntitiesAndCountModel[IndexModelType] | None:
        docs = await self._fetch(query, batch_size)

        if not docs["hits"].get("hits"):
            return None

        return EntitiesAndCountModel[IndexModelType](
            count=docs["hits"]["total"]["value"],
            entities=[self.model_type(**value["_source"]) for value in docs["hits"]["hits"]],
        )

    def query(self) -> QueryBuilder:
        return QueryBuilder(self)


@lru_cache
def get_base_elastic_storage(client: AsyncElasticsearch = Depends(get_elastic)) -> BaseElasticStorage:
    """For servives that don't need data from index"""
    return BaseElasticStorage(client)
