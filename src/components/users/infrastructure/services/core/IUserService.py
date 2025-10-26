from typing import Optional
from zope.interface import Interface

from components.users.web.models.request.UserCreateRequest import UserCreateRequest
from components.users.web.models.request.UserUpdateRequest import UserUpdateRequest
from components.users.web.models.response.UserResponse import UserResponse


class IUserService(Interface):

    async def register_user(self, user_create: UserCreateRequest) -> UserResponse:
        raise NotImplementedError()

    async def login_user(self, email: str, password: str) -> str:
        raise NotImplementedError()

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        raise NotImplementedError()

    async def update_user(self, current_email: str, user_update: UserUpdateRequest) -> UserResponse:
        raise NotImplementedError()
