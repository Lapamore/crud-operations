from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from components.users.infrastructure.models.User import User
from components.users.infrastructure.repository.core.IUserRepository import IUserRepository
from components.users.web.models.request.UserCreateRequest import UserCreateRequest


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self._session.get(User, user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await self._session.execute(query)
        return result.scalars().one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        result = await self._session.execute(query)
        return result.scalars().one_or_none()

    async def create(self, user_data: UserCreateRequest, hashed_password: str) -> User:
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user
    
    async def update(self, user: User, update_data: dict) -> User:
        for key, value in update_data.items():
            setattr(user, key, value)
        
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user