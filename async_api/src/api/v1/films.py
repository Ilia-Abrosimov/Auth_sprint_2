from typing import Optional

from api.utils import Paginator, SortFilmModel, cache, key_builder, parse_sort_dependency
from api.utils.errors import NotFoundException
from api.utils.utils import UserAuthModel, get_current_user
from core.config import settings
from fastapi import APIRouter, Depends
from fastapi.params import Query
from models.film import Film, FilmReviewList
from pydantic import UUID4
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    '/',
    response_model=FilmReviewList,
    responses={
        200: {
            'description': 'Возвращает список фильмов с полями `id`, `title`, `imdb_rating`',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'id': '2a090dde-f688-46fe-a9f4-b781a985275e',
                            'title': 'Star Wars: Knights of the Old Republic',
                            'imdb_rating': 9.6,
                        }
                    ]
                }
            },
        }
    },
)
@cache(
    ttl=settings.FILM_CACHE_EXPIRE_IN_SECONDS,
    key_builder=key_builder('sort,paginator,filter_'),
    response_model=FilmReviewList,
)
async def get_films(
    sort: SortFilmModel = Depends(parse_sort_dependency),
    paginator: Paginator = Depends(),
    filter_: Optional[UUID4] = Query(None, alias='filter[genre]'),
    film_service: FilmService = Depends(get_film_service),
    current_user: UserAuthModel = Depends(get_current_user),
):
    """
    Возвращает список фильмов, отсортированных по полю `imdb_rating` (по возрастанию/по убыванию)
    и фильтрует по id жанра, указанного в поле `filter[genre]`:
    """
    return await film_service.get_many(sort=sort, paginator=paginator, film_filter=filter_)


@router.get(
    '/search',
    response_model=FilmReviewList,
    responses={
        200: {
            'description': 'Возвращает список фильмов с полями `id`, `title`, `imdb_rating`',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'id': '2a090dde-f688-46fe-a9f4-b781a985275e',
                            'title': 'Star Wars: Knights of the Old Republic',
                            'imdb_rating': 9.6,
                        }
                    ]
                }
            },
        }
    },
)
@cache(
    ttl=settings.FILM_CACHE_EXPIRE_IN_SECONDS,
    key_builder=key_builder('query,paginator,sort'),
    response_model=FilmReviewList,
)
async def search_films(
    query: str,
    sort: SortFilmModel = Depends(parse_sort_dependency),
    paginator: Paginator = Depends(),
    film_service: FilmService = Depends(get_film_service),
    current_user: UserAuthModel = Depends(get_current_user),
):
    """
    Поиск по фильмам с сортировкой по полю `imdb_rating` (по возрастанию/по убыванию).

    `query` - искомый текст.
    """
    return await film_service.search_many(sort=sort, paginator=paginator, query_term=query)


@router.get('/{film_id}', response_model=Film)
async def film_details(
    film_id: UUID4,
    film_service: FilmService = Depends(get_film_service),
    current_user: UserAuthModel = Depends(get_current_user),
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise NotFoundException(model=Film, item_id=film_id)

    return film
