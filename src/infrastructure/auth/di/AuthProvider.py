import os
from dishka import Provider, provide, Scope

from infrastructure.auth.core.IAuthService import IAuthService
from infrastructure.auth.impl.AuthService import AuthService


class AuthProvider(Provider):
    @provide(scope=Scope.APP)
    def get_auth_service(self) -> IAuthService:
        return AuthService(
            secret_key=os.getenv("JWT_SECRET"),
            algorithm=os.getenv("ALGORITHM"),
            access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")),
        )