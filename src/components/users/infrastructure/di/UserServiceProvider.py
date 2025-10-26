from dishka import Provider, provide, Scope

from components.users.infrastructure.repository.core.IUserRepository import IUserRepository
from components.users.infrastructure.services.core.IUserService import IUserService
from components.users.infrastructure.services.impl.UserService import UserService


class UserServiceProvider(Provider):

    @provide(scope=Scope.APP)
    def get_user_service(self, user_repo: IUserRepository) -> IUserService:
        return UserService(user_repo)