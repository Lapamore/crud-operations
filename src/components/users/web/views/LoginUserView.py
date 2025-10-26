from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import  Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from components.users.exceptions.InvalidCredentialsException import InvalidCredentialsException
from components.users.infrastructure.services.core.IUserService import IUserService
from components.users.web.models.response.TokenResponse import TokenResponse
from infrastructure.auth.core.IAuthService import IAuthService


class LoginUserView:
    @inject
    async def __call__(
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_service: FromDishka[IUserService] = None,
        auth_service: FromDishka[IAuthService] = None,
    ) -> TokenResponse:
        try:
            user = await user_service.login(
                email=form_data.username, password=form_data.password
            )
            access_token = auth_service.create_access_token(subject=user.id)
            return TokenResponse(access_token=access_token, token_type="bearer")
        except InvalidCredentialsException as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )
