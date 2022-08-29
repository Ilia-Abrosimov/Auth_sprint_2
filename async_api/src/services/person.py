import json
from functools import lru_cache
from typing import Optional

from api.utils import Paginator
from db.elastic import get_elastic
from db.redis import get_redis_cacher
from fastapi import Depends
from models.person import FilmForPerson, Person
from pydantic import UUID4
from services.abstract_cache import AsyncCacheStorage
from services.abstract_db import AsyncStorage
from services.queries import film_for_person
from services.utils import ServiceUtils


class PersonService:
    def __init__(self, persons_utils: ServiceUtils, films_utils: ServiceUtils):
        self.persons_utils = persons_utils
        self.films_utils = films_utils

    async def get_by_id(self, person_id: UUID4) -> Optional[Person]:
        return await self.persons_utils.get(person_id)

    async def search(self, paginator: Paginator, query: str = None) -> Optional[list[Person]]:

        query = {'query': {'multi_match': {'query': query}}}
        return await self.persons_utils.search(
            query=json.dumps(query), size=paginator.page_size, from_=(paginator.page_number - 1) * paginator.page_size
        )

    async def films_for_person(self, person_id: UUID4, paginator: Paginator):
        query = film_for_person(person_id)
        return await self.films_utils.search(
            query=query, size=paginator.page_size, from_=(paginator.page_number - 1) * paginator.page_size
        )


@lru_cache()
def get_person_service(
    cache: AsyncCacheStorage = Depends(get_redis_cacher), storage: AsyncStorage = Depends(get_elastic),
) -> PersonService:
    persons_utils: ServiceUtils = ServiceUtils[Person](Person, 'persons', cache, storage)
    films_utils: ServiceUtils = ServiceUtils[FilmForPerson](FilmForPerson, 'movies', cache, storage)
    return PersonService(persons_utils, films_utils)
