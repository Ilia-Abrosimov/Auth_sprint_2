from api.utils import Paginator, cache, key_builder
from api.utils.errors import NotFoundException
from api.utils.utils import UserAuthModel, get_current_user
from core.config import settings
from fastapi import APIRouter, Depends
from models.genre import Genre, GenreList
from pydantic import UUID4
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get('/', response_model=GenreList)
@cache(ttl=settings.FILM_CACHE_EXPIRE_IN_SECONDS, key_builder=key_builder('paginator'), response_model=GenreList)
async def genres(
    paginator: Paginator = Depends(),
    genre_service: GenreService = Depends(get_genre_service),
    current_user: UserAuthModel = Depends(get_current_user),
):
    """Возвращает список жанров."""
    return await genre_service.get_many(paginator)


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(
    genre_id: UUID4,
    genre_service: GenreService = Depends(get_genre_service),
    current_user: UserAuthModel = Depends(get_current_user),
) -> Genre:
    """Получение жанра по `genre_id`."""
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise NotFoundException(model=Genre, item_id=genre_id)
    return genre
