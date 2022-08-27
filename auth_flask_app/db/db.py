from datetime import timedelta

import redis
from core.config import settings
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
redis_db = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


def init_db(app: Flask):
    app.config[
        'SQLALCHEMY_DATABASE_URI'
    ] = f'postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRES)
    db.init_app(app)
