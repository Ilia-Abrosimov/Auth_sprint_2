from enum import Enum


class RoleTypes(str, Enum):
    # TODO: завести роли в базу
    ADMIN = 'admin'
    USER = 'user'
    PREMIUM = 'premium'
    UNREGISTERED = 'unregistered'
