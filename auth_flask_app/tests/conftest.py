from datetime import timedelta

import pytest
from api.v1.auth import auth
from api.v1.role import role_bp
from api.v1.user import user_bp
from core.config import settings
from db.db import db
from db.db_models import Profile, Role, User, UsersRoles
from extensions import jwt, ma, migrate
from flask import Flask


def init_db(app: Flask):
    app.config[
        'SQLALCHEMY_DATABASE_URI'
    ] = f'postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}' \
        f'@{settings.DB_HOST}:{settings.DB_TEST_HOST_PORT}/{settings.DB_TEST_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRES)
    db.init_app(app)


def create_app():
    test_app = Flask(__name__)
    init_db(test_app)
    migrate.init_app(test_app, db)
    ma.init_app(test_app)
    jwt.init_app(test_app)
    test_app.register_blueprint(auth)
    test_app.register_blueprint(role_bp)
    test_app.register_blueprint(user_bp)
    return test_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        yield app


@pytest.fixture
def test_db():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def test_user():
    user = User(email="Test@test.com")
    user.set_password('qwerty')
    profile1 = Profile(first_name='first_name_Test', last_name='last_name_Test', phone='+7123456789', user=user)
    user2 = User(email="Test2@test.com")
    user2.set_password('qwerty321')
    profile2 = Profile(first_name='first_name_Test2', last_name='last_name_Test2', phone='+7987654321', user=user2)
    db.session.add_all([user, user2, profile1, profile2])
    db.session.commit()
    return user, user2, profile1, profile2


@pytest.fixture
def roles_data():
    user = User(email='admin@admin.com', is_superuser=True)
    user.set_password('password')
    admin_role = Role(name='admin', description='Role for admin')
    user_role = UsersRoles(user=user, role_id=admin_role.id)
    test_role = Role(name='test_role', description='test description')
    simple_user = User(email='simple@user.com')
    simple_user.set_password('simple')
    simple_user_role = UsersRoles(user=simple_user, role_id=test_role.id)
    db.session.add_all([user, admin_role, user_role, test_role, simple_user, simple_user_role])
    db.session.commit()
    return user, admin_role, test_role, user_role, simple_user
