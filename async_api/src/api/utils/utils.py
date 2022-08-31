import dataclasses
import re
from enum import Enum
from http import HTTPStatus

import requests
from api.utils.errors import AccessError, UnauthorizedError
from core.config import settings
from fastapi.params import Query
from fastapi.requests import Request
from pydantic import BaseModel, PositiveInt, parse_obj_as


class UserAuthModel(BaseModel):
    id: str
    is_superuser: bool
    role: str


@dataclasses.dataclass
class Paginator:
    page_size: PositiveInt = Query(default=50, alias='page[size]')
    page_number: PositiveInt = Query(default=1, alias='page[number]')

    def __str__(self):
        return f'{self.page_size}:{self.page_number}'


class SortFilmModel(BaseModel):
    order: str = 'DESC'
    by: str

    def to_query(self):
        return f'{self.by}:{self.order.lower()}'

    def __str__(self):
        return f'{self.by}:{self.order.lower()}'


class SortBy(str, Enum):
    DESC = '-imdb_rating'
    ASC = 'imdb_rating'


def parse_sort_dependency(sort_string: SortBy = SortBy.DESC) -> SortFilmModel:
    order, by = re.findall(re.compile('(-?)(\w+)'), sort_string)[0]
    return SortFilmModel(order='DESC' if order else 'ASC', by=by)


async def get_current_user(request: Request) -> UserAuthModel:
    """Получаем параметры доступа из AUTH"""
    ret = requests.get(
        f'http://{settings.AUTH_HOST}:{settings.AUTH_PORT}/api/v1/auth/verify-jwt', headers=request.headers, timeout=2
    )
    if ret.ok:
        return parse_obj_as(UserAuthModel, ret.json())
    if ret.status_code == HTTPStatus.UNAUTHORIZED:
        raise UnauthorizedError


async def get_admin(request: Request) -> UserAuthModel:
    current_user = await get_current_user(request)
    if current_user.is_superuser or current_user.role == 'admin':
        return current_user
    else:
        raise AccessError(role='admin')
