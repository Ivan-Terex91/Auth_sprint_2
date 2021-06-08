from core.enums import (
    AnonymousUserPermission,
    AuthUserPermission,
    Permissions,
    Roles,
    SuperUserPermission,
)


def insert_user_roles(target, connection, **kw):
    """Добавление ролей при создании таблицы"""
    roles = [{"title": role.value} for role in Roles]
    connection.execute(target.insert(), *roles)


def insert_permissions(target, connection, **kw):
    """Добавление правил при создании таблицы"""
    permissions = [{"title": perm.value} for perm in Permissions]
    connection.execute(target.insert(), *permissions)


def insert_user_role_permissions(target, connection, **kw):
    """Добавление правил в роли при создании таблицы"""
    roles = connection.execute("""SELECT * from role""")
    permissions = connection.execute("""SELECT * from permission""")
    roles = roles.fetchall()
    permissions = permissions.fetchall()

    permissions_anonymous = [
        {"role_id": role[0], "permission_id": permission[0]}
        for role in roles
        if role[1] == "anonymous"
        for permission in permissions
        if permission[1] in [perm.value for perm in AnonymousUserPermission]
    ]

    permissions_auth = [
        {"role_id": role[0], "permission_id": permission[0]}
        for role in roles
        if role[1] == "authenticated"
        for permission in permissions
        if permission[1] in [perm.value for perm in AuthUserPermission]
    ]

    permissions_superuser = [
        {"role_id": role[0], "permission_id": permission[0]}
        for role in roles
        if role[1] == "superuser"
        for permission in permissions
        if permission[1] in [perm.value for perm in SuperUserPermission]
    ]

    connection.execute(
        target.insert(), *permissions_anonymous, *permissions_auth, *permissions_superuser
    )
