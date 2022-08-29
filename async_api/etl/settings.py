from pydantic import BaseModel, BaseSettings


class ElasticConfig(BaseModel):
    host: str
    port: int


class RedisConfig(BaseModel):
    host: str
    port: int


class PostgresConfig(BaseModel):
    name: str = 'movies_database'
    user: str = 'postgres'
    password: str = ''
    host: str = 'localhost'
    port: int = 5432


class Settings(BaseSettings):
    batch_size: int = 100
    indexes: list[str] = ['movies', 'genres', 'persons']
    frequency: int = 10
    db: PostgresConfig
    elasticsearch: ElasticConfig
    redis: RedisConfig
    redis_key: str = 'movies'

    class Config:
        env_nested_delimiter = '__'
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
