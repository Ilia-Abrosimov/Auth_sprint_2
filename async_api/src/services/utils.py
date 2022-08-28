from typing import Generic, Optional, TypeVar

from core.config import settings
from elasticsearch import NotFoundError
from pydantic import UUID4
from services.abstract_cache import AsyncCacheStorage
from services.abstract_db import AsyncStorage

T = TypeVar('T')


def get_films_es_utils(model: T) -> 'ServiceUtils':
    return ServiceUtils[model]


class ServiceUtils(Generic[T]):
    def __init__(self, model: T, index: str, cache: AsyncCacheStorage, storage: AsyncStorage):
        self.cache = cache
        self.storage = storage
        self._index = index
        self._model = model

    async def get(self, item_id: UUID4) -> Optional[T]:
        item = await self._item_from_cache(item_id)
        if item:
            return item
        try:
            raw_item = await self.storage.get(self._index, item_id)
        except NotFoundError:
            return None
        item = self._model(**raw_item['_source'])
        await self._put_item_to_cache(item)
        return item

    async def get_all(self, page_size, from_=0) -> list[T]:
        doc = await self.storage.search(index=self._index, size=page_size, from_=from_)
        return [self._model(**d['_source']) for d in doc['hits']['hits']]

    async def storage_search(self, query: str, sort: str = "", size=50, from_=0) -> Optional[list[T]]:
        try:
            docs = await self.storage.search(index=self._index, body=query, sort=sort, size=size, from_=from_)
        except NotFoundError:
            return None
        return [self._model(**doc['_source']) for doc in docs['hits']['hits']]

    async def search(self, query: str, size=50, from_=0) -> Optional[list[T]]:
        try:
            docs = await self.storage.search(index=self._index, body=query, size=size, from_=from_)
        except NotFoundError:
            return None
        return [self._model(**doc['_source']) for doc in docs['hits']['hits']]

    async def _item_from_cache(self, item_id: UUID4) -> Optional[T]:
        data = await self.cache.get(self._build_key(item_id))
        if not data:
            return None
        return self._model.parse_raw(data)

    async def _put_item_to_cache(self, item: T):
        await self.cache.set(self._build_key(item.id), item.json(), expire=settings.FILM_CACHE_EXPIRE_IN_SECONDS)

    def _build_key(self, item_id):
        return f'{self._index}:{item_id}'
