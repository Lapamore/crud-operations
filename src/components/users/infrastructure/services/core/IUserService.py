from abc import ABC, abstractmethod
from typing import Optional

from components.users.web.models.request.UserCreateRequest import UserCreateRequest
from components.users.web.models.request.UserUpdateRequest import UserUpdateRequest
from components.users.infrastructure.models.User import User


class IUserService(ABC):

    @abstractmethod
    async def register(self, user_create: UserCreateRequest) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def login(self, email: str, password: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, user: User, user_update: UserUpdateRequest) -> User:
        raise NotImplementedError()
