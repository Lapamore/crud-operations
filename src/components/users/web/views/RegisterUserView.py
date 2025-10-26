from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

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
        user = await user_service.register(user_create)
        token = auth_service.create_token(user.email)
        user.token = token
        return UserResponse.model_validate(user)
