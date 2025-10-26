from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import HTTPException, status

from components.users.exceptions.UserAlreadyExistsException import UserAlreadyExistsException
from components.users.infrastructure.services.core.IUserService import IUserService
from components.users.web.models.request.UserCreateRequest import UserCreateRequest
from components.users.web.models.response.UserResponse import UserResponse
from infrastructure.auth.core.IAuthService import IAuthService


class RegisterUserView:
    @inject
    async def __call__(
        self,
        user_create: UserCreateRequest,
        user_service: FromDishka[IUserService],
        auth_service: FromDishka[IAuthService],
    ) -> UserResponse:
        try:
            user = await user_service.register(user_create)
            token = auth_service.create_access_token(subject=user.email)
            user.token = token
            return UserResponse.model_validate(user)
        except UserAlreadyExistsException as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
