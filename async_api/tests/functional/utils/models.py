from pydantic import UUID4, BaseModel


class PersonResponseModel(BaseModel):
    id: UUID4
    name: str
    role: list[str]
    film_ids: list[str]

    class Config:
        extra = 'forbid'


class FilmReviewResponseModel(BaseModel):
    id: UUID4
    title: str
    imdb_rating: float

    class Config:
        extra = 'forbid'
