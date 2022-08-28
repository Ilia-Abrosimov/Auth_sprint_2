from models.base import MainModel
from pydantic import BaseModel


class Person(MainModel):
    name: str
    role: list[str]
    film_ids: list[str]


class FilmForPerson(MainModel):
    title: str
    imdb_rating: float


class PersonList(BaseModel):
    __root__: list[Person]


class FilmForPersonList(BaseModel):
    __root__: list[FilmForPerson]
