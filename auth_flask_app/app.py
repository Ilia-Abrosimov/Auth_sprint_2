from api.v1.auth import auth
from api.v1.ouath.google import oauth_google
from api.v1.ouath.yandex import oauth_yandex
from api.v1.role import role_bp
from api.v1.user import user_bp
from cli.commands import cli_bp
from core.config import settings
from core.swagger_config import swagger_config
from db.db import db, init_db
from extensions import jwt, ma, migrate, oauth
from flasgger import Swagger
from flask import Flask, request
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)
init_db(app)
migrate.init_app(app, db)
ma.init_app(app)
jwt.init_app(app)
oauth.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(role_bp)
app.register_blueprint(user_bp)
app.register_blueprint(oauth_yandex)
app.register_blueprint(oauth_google)
app.register_blueprint(cli_bp)
Swagger(app, config=swagger_config)
FlaskInstrumentor().instrument_app(app)


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is required')


def main():
    app.run(host=settings.APP_HOST, debug=settings.DEBUG)


if __name__ == '__main__':
    main()
