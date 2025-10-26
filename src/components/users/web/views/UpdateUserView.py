from fastapi import Depends, HTTPException, status
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from components.users.exceptions.UserAlreadyExistsException import UserAlreadyExistsException
from components.users.infrastructure.models.User import User
from components.users.infrastructure.services.core.IUserService import IUserService
from components.users.web.models.request.UserUpdateRequest import UserUpdateRequest
from components.users.web.models.response.UserResponse import UserResponse


class UpdateUserView:
    @inject
    async def update_user_view(
        user_update: UserUpdateRequest,
        user_service: FromDishka[IUserService] = None,
        current_user: User = Depends(get_current_user)
    ) -> UserResponse:
        try:
            updated_user = await user_service.update(current_user, user_update)
            return UserResponse.model_validate(updated_user)
        except UserAlreadyExistsException as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
