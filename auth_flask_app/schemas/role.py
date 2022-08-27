from db.db_models import Role
from extensions import ma
from marshmallow import EXCLUDE


class FullRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        unknown = EXCLUDE
        load_instance = True


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        exclude = ('id',)
        unknown = EXCLUDE
        load_instance = True


full_role_schema = FullRoleSchema()
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
