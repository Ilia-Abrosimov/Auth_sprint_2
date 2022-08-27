from enum import Enum


class RoleTypes(str, Enum):
    # TODO: добавить роли и завести эти роли в базу
    ADMIN = 'admin'
    USER = 'user'
    PREMIUM = 'premium'
