from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_PASSWORD: str = 'password'
    DB_USER: str = 'user'
    DB_NAME: str = 'postgres'
    DB_HOST: str = 'localhost'
    DB_TEST_HOST_PORT: int = 5442
    DB_TEST_NAME: str = 'postgrestest'
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    APP_HOST: str = '0.0.0.0'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    JWT_SECRET_KEY: str = 'top_secret'
    JWT_ACCESS_TOKEN_EXPIRES: int = 1
    DEBUG: bool = False
    API_URL: str = "http://127.0.0.1:5000/api/v1/"

    class Config:
        env_file = '.env'


settings = Settings()
