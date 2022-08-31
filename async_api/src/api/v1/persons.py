from api.utils import Paginator, cache, key_builder
from api.utils.errors import NotFoundException
from api.utils.utils import UserAuthModel, get_current_user
from core.config import settings
from fastapi import APIRouter, Depends
from models.person import FilmForPersonList, Person, PersonList
from pydantic import UUID4
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/search', response_model=PersonList)
@cache(ttl=settings.FILM_CACHE_EXPIRE_IN_SECONDS, key_builder=key_builder('query,paginator'), response_model=PersonList)
async def search_persons(
    query: str,
    paginator: Paginator = Depends(),
    person_service: PersonService = Depends(get_person_service),
    current_user: UserAuthModel = Depends(get_current_user),
):
    """Поиск персоналий по тексту в `query`"""
    persons = await person_service.search(paginator=paginator, query=query)
    return persons


@router.get('/{person_id}', response_model=Person)
async def person_details(
    person_id: UUID4,
    person_service: PersonService = Depends(get_person_service),
    current_user: UserAuthModel = Depends(get_current_user),
) -> Person:
    """Получение персоналии по `person_id`."""
    person = await person_service.get_by_id(person_id)
    if not person:
        raise NotFoundException(model=Person, item_id=person_id)
    return person


@router.get('/{person_id}/film', response_model=FilmForPersonList)
@cache(
    ttl=settings.FILM_CACHE_EXPIRE_IN_SECONDS,
    key_builder=key_builder('person_id,paginator'),
    response_model=FilmForPersonList,
)
async def person_films(
    person_id: UUID4,
    paginator: Paginator = Depends(),
    person_service: PersonService = Depends(get_person_service),
    current_user: UserAuthModel = Depends(get_current_user),
):
    """Получение списка всех фильмов, в которых принимал участие человек."""
    person = await person_service.films_for_person(person_id, paginator=paginator)
    if not person:
        raise NotFoundException(model=FilmForPersonList, item_id=person_id)
    return person
