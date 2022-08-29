from functools import lru_cache
from typing import Optional

from api.utils import Paginator
from db.elastic import get_elastic
from db.redis import get_redis_cacher
from fastapi import Depends
from models.genre import Genre
from pydantic import UUID4
from services.abstract_cache import AsyncCacheStorage
from services.abstract_db import AsyncStorage
from services.utils import ServiceUtils


class GenreService:
    def __init__(self, genres_utils: ServiceUtils):
        self.genres_utils = genres_utils

    async def get_by_id(self, genre_id: UUID4) -> Optional[Genre]:
        return await self.genres_utils.get(genre_id)

    async def get_many(self, paginator: Paginator):
        return await self.genres_utils.get_all(
            page_size=paginator.page_size, from_=(paginator.page_number - 1) * paginator.page_size
        )


@lru_cache()
def get_genre_service(
    cache: AsyncCacheStorage = Depends(get_redis_cacher), storage: AsyncStorage = Depends(get_elastic),
) -> GenreService:
    genres_utils: ServiceUtils = ServiceUtils[Genre](Genre, 'genres', cache, storage)
    return GenreService(genres_utils)
