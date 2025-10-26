from abc import ABC, abstractmethod
from typing import Optional

from components.users.infrastructure.models.User import User
from components.users.web.models.request.UserCreateRequest import UserCreateRequest


class IUserRepository(ABC):

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError()
    
    @abstractmethod
    async def create(self, user: UserCreateRequest, hashed_password) -> User:
        raise NotImplementedError()
    
    @abstractmethod
    async def update(self, user: User, update_data: dict) -> User:
        raise NotImplementedError()