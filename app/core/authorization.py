from fastapi import Depends, HTTPException, Request
from starlette import status

from core.auth import get_current_user


async def authorize_user(
    request: Request, current_user: get_current_user = Depends(get_current_user)
):
    authorization_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden, you don't have permission to access",
    )

    mapper_endpoint_permission = {
        "get_film_details": "movies_get_film",
        "post_film_details": "movies_create_film",
        "put_film_details": "movies_change_film",
        "delete_film_details": "movies_delete_film",
        "get_film_list": "movies_get_film_list",
        "get_genre_details": "movies_get_genre",
        "post_genre_details": "movies_create_genre",
        "put_genre_details": "movies_change_genre",
        "delete_genre_details": "movies_delete_genre",
        "get_genre_list": "movies_get_genre_list",
        "get_person_details": "movies_get_person",
        "post_person_details": "movies_create_person",
        "put_person_details": "movies_change_person",
        "delete_person_details": "movies_delete_person",
        "person_film_list": "movies_get_person_list",
        "get_film_search": "movies_search_film",
        "get_person_search": "movies_search_person",
    }

    endpoint = "_".join((request.get("method").lower(), request.get("endpoint").__name__))
    permission_name = mapper_endpoint_permission[endpoint]

    if permission_name not in current_user.user_permissions:
        raise authorization_exception


async def is_adult_user(current_user: get_current_user = Depends(get_current_user)) -> bool:
    return "adult" in current_user.user_roles
