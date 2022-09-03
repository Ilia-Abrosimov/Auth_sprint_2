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
    SESSION_SECRET: str = 'secret'
    YANDEX_CLIENT_ID: str = 'secret'
    YANDEX_CLIENT_SECRET: str = 'secret'
    YANDEX_AUTH_URL: str = 'secret'
    GOOGLE_CLIENT_ID: str = 'secret'
    GOOGLE_CLIENT_SECRET: str = 'secret'
    GOOGLE_AUTH_URL: str = 'secret'
    JAEGER_UDP: int = 6831
    JAEGER_HOST_NAME: str = 'jaeger'
    REQUEST_LIMIT_PER_MINUTE: int = 20

    class Config:
        env_file = '.env'


settings = Settings()
