from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from components.users.infrastructure.repository.core.IUserRepository import IUserRepository
from components.users.infrastructure.repository.impl.UserRepository import UserRepository


class UserInfrastructureProvider(Provider):

    @provide(scope=Scope.APP)
    def get_user_repository(self, session: AsyncSession) -> IUserRepository:
        return UserRepository(session)