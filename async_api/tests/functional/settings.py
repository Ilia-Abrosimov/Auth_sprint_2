from pydantic import BaseSettings


class Settings(BaseSettings):
    API_HOST: str = '127.0.0.1'
    API_PORT: int = 9000
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379
    ES_HOST: str = '127.0.0.1'
    ES_PORT: int = 9200

    class Config:
        env_file = '.env'


settings = Settings()
