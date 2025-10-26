from typing import Optional

from sqlalchemy import select
from zope.interface import implementer
from sqlalchemy.ext.asyncio import AsyncSession

from components.users.infrastructure.models.User import User
from components.users.infrastructure.repository.core.IUserRepository import IUserRepository


@implementer(IUserRepository)
class UserRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self.__session.get(User, user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await self.__session.execute(query)
        return result.scalars().one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        result = await self.__session.execute(query)
        return result.scalars().one_or_none()