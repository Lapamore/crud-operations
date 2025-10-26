from dishka import Provider, provide, Scope

from components.users.infrastructure.repository.core.IUserRepository import IUserRepository
from components.users.infrastructure.services.core.IUserService import IUserService
from components.users.infrastructure.services.impl.UserService import UserService
from infrastructure.auth.core.IAuthService import IAuthService


class UserServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_service(
        self,
        user_repo: IUserRepository,
        auth_service: IAuthService,
    ) -> IUserService:
        return UserService(user_repo, auth_service)