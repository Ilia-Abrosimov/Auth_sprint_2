import json
from functools import lru_cache
from typing import Optional

from api.utils import Paginator, SortFilmModel
from db.elastic import get_elastic
from db.redis import get_redis_cacher
from fastapi import Depends
from models.film import Film
from models.genre import Genre
from pydantic import UUID4
from services.abstract_cache import AsyncCacheStorage
from services.abstract_db import AsyncStorage
from services.utils import ServiceUtils


class FilmService:
    def __init__(self, films_utils: ServiceUtils, genres_utils: ServiceUtils):
        self.films_utils = films_utils
        self.genres_utils = genres_utils

    async def get_by_id(self, film_id: UUID4) -> Optional[Film]:
        return await self.films_utils.get(film_id)

    async def get_many(self, sort: SortFilmModel, paginator: Paginator, film_filter: UUID4 = None) -> list[Film]:
        if film_filter:
            ret = await self._filter_films(
                sort=sort.to_query(),
                size=paginator.page_size,
                from_=(paginator.page_number - 1) * paginator.page_size,
                genre_id=film_filter,
            )
        else:
            ret = await self.search_many(sort=sort, paginator=paginator, query_term='*')
        return ret

    async def search_many(self, sort: SortFilmModel, paginator: Paginator, query_term: str = None) -> list[Film]:
        query = {'query': {'query_string': {'query': query_term}}}
        ret = await self.films_utils.storage_search(
            sort=sort.to_query(),
            size=paginator.page_size,
            from_=(paginator.page_number - 1) * paginator.page_size,
            query=json.dumps(query),
        )
        return ret

    async def _filter_films(self, genre_id: UUID4, sort: str = "", size=50, from_=0) -> Optional[list[Film]]:
        genre = await self.genres_utils.get(genre_id)
        if not genre:
            return None
        query = {'query': {'term': {'genre': {'value': genre.name}}}}
        return await self.films_utils.storage_search(query=json.dumps(query), sort=sort, size=size, from_=from_)


@lru_cache()
def get_film_service(
    cache: AsyncCacheStorage = Depends(get_redis_cacher), storage: AsyncStorage = Depends(get_elastic),
) -> FilmService:
    films_utils: ServiceUtils = ServiceUtils[Film](Film, 'movies', cache, storage)
    genres_utils: ServiceUtils = ServiceUtils[Genre](Genre, 'genres', cache, storage)

    return FilmService(films_utils, genres_utils)
