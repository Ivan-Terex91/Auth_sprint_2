from enum import Enum
from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4, BaseModel

from core.auth import get_current_user
from core.authorization import AuthorizedUser
from services.genre import GenreService, get_genre_service

router = APIRouter()


class Genre(BaseModel):
    """Модель ответа для жанров"""

    id: UUID4
    name: str


class SortFields(Enum):
    """Поля по которым можно делать сортировку"""

    id__asc = "id"
    id__desc = "-id"
    name__asc = "name"
    name__desc = "-name"


@router.get(
    "/{genre_id:uuid}/",
    response_model=Genre,
    dependencies=[Depends(AuthorizedUser("movies_get_genre"))],
)
async def genre_details(
    genre_id: UUID,
    genre_service: GenreService = Depends(get_genre_service),
    current_user=Depends(get_current_user),
) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")
    return Genre(id=genre.id, name=genre.name)


@router.get(
    "/", response_model=List[Genre], dependencies=[Depends(AuthorizedUser("movies_get_genre_list"))]
)
async def genre_list(
    page: Optional[int] = 1,
    size: Optional[int] = 50,
    sort: Optional[SortFields] = SortFields.name__asc,
    genre_service: GenreService = Depends(get_genre_service),
    current_user=Depends(get_current_user),
) -> List[Genre]:
    sort_value, sort_order = sort.name.split("__")
    genres = await genre_service.get_genres_list(
        page=page, size=size, sort_value=sort_value, sort_order=sort_order
    )
    return [Genre(id=genre.id, name=genre.name) for genre in genres]
