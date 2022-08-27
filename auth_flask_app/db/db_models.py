import uuid
from datetime import datetime

from db.db import db
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    login_history = db.relationship('LoginHistory', backref='user', lazy='dynamic')
    role = db.relationship('UsersRoles', backref='user', lazy='dynamic')
    profile = db.relationship('Profile', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone = db.Column(db.String)

    def __repr__(self):
        return f'<Profile {self.first_name} {self.last_name}>'


class LoginHistory(db.Model):
    __tablename__ = 'login_histories'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    user_agent = db.Column(db.String, nullable=False)
    authentication_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<LoginHistory {self.authentication_date}>'


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    users = db.relationship('UsersRoles', backref='users', lazy='dynamic')
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)

    def __repr__(self):
        return f'<Role {self.name}>'


class UsersRoles(db.Model):
    __tablename__ = 'usersroles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), unique=True)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('role.id'))

    def __repr__(self):
        return f'<Role {self.role_id} for user {self.user_id}>'
