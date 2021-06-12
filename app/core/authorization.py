from datetime import date

from fastapi import Depends, HTTPException
from starlette import status

from core.auth import get_current_user

from .enums import AdultAgeCountry


class AuthorizedUser:
    def __init__(self, permission_name: str):
        self.permission_name = permission_name

    async def __call__(self, current_user: get_current_user = Depends(get_current_user)):
        authorization_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden, you don't have permission to access",
        )

        if self.permission_name not in current_user.user_permissions:
            raise authorization_exception


async def is_adult_user(current_user: get_current_user = Depends(get_current_user)) -> bool:
    user_country_age_adult = AdultAgeCountry[current_user.country]
    if current_user.birthdate:
        return (date.today().year - current_user.birthdate.year) >= user_country_age_adult
    return False
