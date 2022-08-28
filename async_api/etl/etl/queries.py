from enum import Enum
from typing import Optional


class PersonTypes(str, Enum):
    DIRECTOR = 'director'
    ACTOR = 'actor'
    WRITER = 'writer'


def get_movies_query(start_date: Optional[str]):
    return f"""
    SELECT film.id,
        film.rating AS imdb_rating,
        film.title,
        film.description,
        film.type,
        ARRAY_AGG(DISTINCT jsonb_build_object('id', genre.id, 'name', genre.name)) AS genres,
        ARRAY_AGG(DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name)) 
            FILTER (WHERE person_film.role = '{PersonTypes.DIRECTOR}') AS directors,
        ARRAY_AGG(DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name)) 
            FILTER (WHERE person_film.role = '{PersonTypes.ACTOR}') AS actors,
        ARRAY_AGG(DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name)) 
            FILTER (WHERE person_film.role = '{PersonTypes.WRITER}') AS writers,
        GREATEST(film.modified, MAX(person.modified), MAX(genre.modified)) AS updated_at
    FROM content.film_work AS film
        LEFT JOIN content.genre_film_work AS genre_film ON film.id = genre_film.film_work_id
        LEFT JOIN content.genre AS genre ON genre_film.genre_id = genre.id
        LEFT JOIN content.person_film_work AS person_film ON film.id = person_film.film_work_id
        LEFT JOIN content.person AS person ON person_film.person_id = person.id
    WHERE
        GREATEST(film.modified, person.modified, genre.modified) > '{start_date}'
    GROUP BY film.id
    ORDER BY GREATEST(film.modified, MAX(person.modified), MAX(genre.modified)) ASC

        """


def get_genres_query(start_date: Optional[str]):
    return f"""
    SELECT genre.id,
        genre.name,
        genre.description,
        genre.modified AS updated_at
    FROM content.genre AS genre
    WHERE
        genre.modified > '{start_date}'
    GROUP BY genre.id
    ORDER BY genre.modified ASC
        """


def get_persons_query(start_date: Optional[str]):
    return f"""
    SELECT person.id,
        person.full_name AS name,
        ARRAY_AGG(DISTINCT person_film.role::text) AS role,
        ARRAY_AGG(DISTINCT person_film.film_work_id::text) AS film_ids,
        person.modified AS updated_at
    FROM content.person AS person
        LEFT JOIN content.person_film_work AS person_film ON person.id = person_film.person_id
    WHERE
        person.modified > '{start_date}'
    GROUP BY person.id
    ORDER BY person.modified ASC
        """
