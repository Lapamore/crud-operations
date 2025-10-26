from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

from components.users.infrastructure.repository.core.IUserRepository import IUserRepository
from components.users.web.models.response.UserResponse import UserResponse
from infrastructure.auth.core.IAuthService import IAuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

class GetCurrentUserView:
    @inject
    async def __call__(
        self,
        auth_service: FromDishka[IAuthService],
        user_repo: FromDishka[IUserRepository],
        token: str = Depends(oauth2_scheme)
    ) -> UserResponse:
        user_id = auth_service.get_current_user_id(token)

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = user_repo.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return UserResponse.model_validate(user)

