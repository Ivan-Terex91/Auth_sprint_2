import logging

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from httpx import HTTPError
from pydantic import UUID4

from core.models import BaseModel

logger = logging.getLogger(__name__)


class AuthClient:
    def __init__(self, base_url):
        self.base_url = base_url

    async def check_token(self, token: str):
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            return await client.post("/staff/api/v1/auth/check_token/", json={"token": token})


auth_client: AuthClient = None


def get_auth_client() -> AuthClient:
    return auth_client


class User(BaseModel):
    user_id: UUID4
    first_name: str
    last_name: str


api_token_scheme = APIKeyHeader(name="TOKEN")


async def get_current_user(
    token: str = Depends(api_token_scheme), auth_client: AuthClient = Depends(get_auth_client)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate access token",
    )

    try:
        response = await auth_client.check_token(token)
    except HTTPError as exc:
        logger.error(f"Auth request failed: {exc!r}")
        raise credentials_exception

    if response.status_code != status.HTTP_200_OK:
        raise credentials_exception

    data = response.json()

    return User(
        user_id=data["user_id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
    )
