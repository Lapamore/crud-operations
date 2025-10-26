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
    ):
        try:
            user = await user_service.register(user_create)
            access_token = auth_service.create_access_token(subject=user.id)
            
            user_response = UserResponse.model_validate(user)
            
            response_data = {
                "user": user_response.model_dump(),
                "access_token": access_token,
                "token_type": "bearer",
            }
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=response_data
            )
        except UserAlreadyExistsException as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
