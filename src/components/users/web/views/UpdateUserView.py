from fastapi import Depends, HTTPException, status
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from components.users.exceptions.UserAlreadyExistsException import UserAlreadyExistsException
from components.users.infrastructure.models.User import User
from components.users.infrastructure.services.core.IUserService import IUserService
from components.users.web.models.request.UserUpdateRequest import UserUpdateRequest
from components.users.web.models.response.UserResponse import UserResponse
from components.users.web.dependencies import get_current_user


class UpdateUserView:
    @inject
    async def __call__(
        self,
        user_service: FromDishka[IUserService],
        user_update: UserUpdateRequest,
        current_user: User = Depends(get_current_user),
    ) -> UserResponse:
        user = await user_service.update_user(current_user, user_update)
        return UserResponse.model_validate(user)
