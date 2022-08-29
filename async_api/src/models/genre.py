from models.base import MainModel
from pydantic import BaseModel


class Genre(MainModel):
    name: str


class GenreList(BaseModel):
    __root__: list[Genre]
