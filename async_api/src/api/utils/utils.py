import dataclasses
import re
from enum import Enum

from fastapi.params import Query
from pydantic import BaseModel, PositiveInt


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
