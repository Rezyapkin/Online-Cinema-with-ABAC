from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Request


@lru_cache
def get_elastic(request: Request) -> AsyncElasticsearch:
    """Get Elasticsearch connection."""
    return request.app.state.es
