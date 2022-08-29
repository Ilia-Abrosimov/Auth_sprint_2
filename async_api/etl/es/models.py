from enum import Enum
from typing import Optional

from pydantic import UUID4, BaseModel, Field


class PersonType(str, Enum):
    actor = 'actor'
    director = 'director'
    writer = 'writer'


class UUIDMixin(BaseModel):
    id: UUID4


class PersonInFilm(UUIDMixin):
    name: str


class MoviesES(UUIDMixin):
    elasticsearch_id: UUID4 = Field(..., alias='_id')
    title: str
    imdb_rating: Optional[float] = None
    genre: Optional[list[str]] = None
    description: Optional[str] = None
    director: Optional[list[str]] = []
    actors_names: Optional[list[str]] = None
    writers_names: Optional[list[str]] = None
    actors: Optional[list[PersonInFilm]] = None
    writers: Optional[list[PersonInFilm]] = None

    def __init__(self, *args, **kwargs):
        ret = {}
        for key in kwargs:
            if key == 'genres':
                ret['genre'] = [x['name'] for x in kwargs[key]]
            elif key in ('actors', 'writers') and kwargs[key] is not None:
                ret[f'{key}_names'] = [x['name'] for x in kwargs[key]]
                ret[key] = kwargs[key]
            elif key == 'directors' and kwargs[key]:
                ret['director'] = [x['name'] for x in kwargs[key]]
            elif key == 'id':
                ret['_id'] = kwargs[key]
                ret['id'] = kwargs[key]
            else:
                ret[key] = kwargs[key]
        super().__init__(**ret)


class GenresES(UUIDMixin):
    elasticsearch_id: UUID4 = Field(..., alias='_id')
    name: str
    description: Optional[str] = None

    def __init__(self, *args, **kwargs):
        ret = {}
        for key in kwargs:
            if key == 'id':
                ret['_id'] = kwargs[key]
                ret['id'] = kwargs[key]
            else:
                ret[key] = kwargs[key]
        super().__init__(**ret)


class PersonsES(PersonInFilm):
    elasticsearch_id: UUID4 = Field(..., alias='_id')
    role: Optional[list[PersonType]] = None
    film_ids: Optional[list[UUID4]] = None

    def __init__(self, *args, **kwargs):
        ret = {}
        for key in kwargs:
            if key == 'id':
                ret['_id'] = kwargs[key]
                ret['id'] = kwargs[key]
            else:
                ret[key] = kwargs[key]
        super().__init__(**ret)
