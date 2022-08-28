from typing import Optional

from models.base import MainModel
from pydantic import UUID4, BaseModel, Field


class Person(MainModel):
    name: str


class Film(MainModel):
    title: str
    description: Optional[str]
    actors: Optional[list[Person]]
    actors_names: Optional[list[str]]
    director: Optional[list[str]]
    genre: Optional[list[str]]
    imdb_rating: Optional[float]
    writers: Optional[list[Person]]
    writers_names: Optional[list[str]]


class FilmReview(BaseModel):
    uuid: UUID4 = Field(..., alias='id')
    title: str
    imdb_rating: float


class FilmReviewList(BaseModel):
    __root__: list[FilmReview]
