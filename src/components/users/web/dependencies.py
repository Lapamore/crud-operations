from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from components.users.infrastructure.models import User
from components.users.infrastructure.repository.core.IUserRepository import IUserRepository
from infrastructure.auth.core.IAuthService import IAuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


@inject
async def get_current_user(
    auth_service: Annotated[IAuthService, FromDishka()],
    user_repo: Annotated[IUserRepository, FromDishka()],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    user_id = auth_service.get_current_user_id(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
