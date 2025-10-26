from zope.interface import Interface
from typing import Optional

from components.users.infrastructure.models.User import User


class IUserRepository(Interface):

    async def get_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError()

    async def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError()