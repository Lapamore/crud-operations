from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.components.users.infrastructure.repository.core.IUserRepository import (
    IUserRepository,
)
from src.components.users.web.models.response.ProfileResponse import ProfileResponse
from src.infrastructure.auth.core.IAuthService import IAuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


class GetCurrentUserView:
    @inject
    async def __call__(
        self,
        token: str = Depends(oauth2_scheme),
        user_repo: FromDishka[IUserRepository] = None,
        auth_service: FromDishka[IAuthService] = None,
    ) -> ProfileResponse:
        user_id = auth_service.get_current_user_id(token)
        user = await user_repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return ProfileResponse.model_validate(user)

