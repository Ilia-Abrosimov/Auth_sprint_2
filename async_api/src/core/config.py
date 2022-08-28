from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    PROJECT_NAME: str = 'movies'
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    ELASTIC_HOST: str = 'localhost'
    ELASTIC_PORT: int = 9200
    FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5
    DEFAULT_CACHE_TTL = 60 * 5

    class Config:
        env_file = '.env'


settings = Settings()
