from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from components.users.infrastructure.repository.core.IUserRepository import IUserRepository
from components.users.infrastructure.repository.impl.UserRepository import UserRepository


class UserRepoProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_repo(self, session: AsyncSession) -> IUserRepository:
        return UserRepository(session)