from enum import Enum

from core.utils import extend_enum


class Action(Enum):
    """Действия пользователя."""

    login = "login"
    logout = "logout"


class DeviceType(Enum):
    """Типы устройств пользователя."""

    pc = "pc"
    mobile = "mobile"
    tablet = "tablet"
    undefined = "undefined"


class Roles(Enum):
    """Роли пользователя."""

    authenticated = "authenticated"
    anonymous = "anonymous"
    adult = "adult"
    superuser = "superuser"


class Permissions(Enum):
    """Все действия приложения фильмов"""

    movies_get_film = "movies_get_film"
    movies_create_film = "movies_create_film"
    movies_change_film = "movies_change_film"
    movies_delete_film = "movies_delete_film"
    movies_get_film_list = "movies_get_film_list"

    movies_get_genre = "movies_get_genre"
    movies_create_genre = "movies_create_genre"
    movies_change_genre = "movies_change_genre"
    movies_delete_genre = "movies_delete_genre"
    movies_get_genre_list = "movies_get_genre_list"

    movies_get_person = "movies_get_person"
    movies_create_person = "movies_create_person"
    movies_change_person = "movies_change_person"
    movies_delete_person = "movies_delete_person"
    movies_get_person_list = "movies_get_person_list"

    movies_search_film = "movies_search_film"
    movies_search_person = "movies_search_person"


class AnonymousUserPermission(Enum):
    """Действия для анонимных пользователей"""

    movies_get_film = "movies_get_film"
    movies_get_film_list = "movies_get_film_list"
    movies_get_genre = "movies_get_genre"
    movies_get_genre_list = "movies_get_genre_list"
    movies_get_person = "movies_get_person"
    movies_get_person_list = "movies_get_person_list"


@extend_enum(AnonymousUserPermission)
class AuthUserPermission(Enum):
    """Действия для аутентифицированных пользователей"""

    movies_search_film = "movies_search_film"
    movies_search_person = "movies_search_person"


@extend_enum(Permissions)
class SuperUserPermission(Enum):
    """Действия для супер пользователей"""

    pass


class OAuthProvider(Enum):
    facebook = "facebook"
