from typing import Optional

from elasticsearch import AsyncElasticsearch
from services.abstract_db import AsyncStorage

es: Optional[AsyncElasticsearch] = None


class ElasticSearchStorage(AsyncStorage):
    def __init__(self, es_: AsyncElasticsearch):
        self._es = es_

    async def get(self, index, item_id, doc_type=None, params=None, headers=None, **kwargs):
        return await self._es.get(index, item_id, doc_type=doc_type, params=params, headers=headers, **kwargs)

    async def search(self, body=None, index=None, doc_type=None, params=None, headers=None, **kwargs):
        return await self._es.search(
            body=body, index=index, doc_type=doc_type, params=params, headers=headers, **kwargs
        )


async def get_elastic() -> AsyncStorage:
    return ElasticSearchStorage(es)
