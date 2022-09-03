from authlib.integrations.flask_client import OAuth
from core.config import app_config
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()
oauth = OAuth()
cache = Cache(config=app_config)
