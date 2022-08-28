from db.db_models import LoginHistory, Profile, User
from extensions import ma
from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import auto_field


class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        exclude = ('id', 'user_id')
        unknown = EXCLUDE
        load_instance = True


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('is_active', 'is_superuser', 'date_joined', 'login_history', 'role', 'profile', 'password_hash')
        load_only = ('password_hash',)
        unknown = EXCLUDE
        load_instance = True

    password = auto_field("password_hash")


class UserProfileSchema(ma.Schema):
    email = ma.String(required=True)
    password = ma.String(required=True)
    first_name = ma.String()
    last_name = ma.String()
    phone = ma.String()


class PasswordSchema(ma.Schema):
    old_password = ma.String(required=True)
    new_password = ma.String(required=True)


class LoginHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LoginHistory
        exclude = ('id', 'user_id')


class UserRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('email', 'is_active', 'date_joined', 'login_history', 'profile', 'password_hash')
        unknown = EXCLUDE
        load_instance = True


profile_schema = ProfileSchema()
user_schema = UserSchema()
user_profile_schema = UserProfileSchema()
password_schema = PasswordSchema()
login_history_schema = LoginHistorySchema()
user_role_schema = UserRoleSchema()
