from typing import Optional

from infrastructure.auth.core import IAuthService
from components.users.exceptions.InvalidCredentialsException import InvalidCredentialsException
from components.users.exceptions.UserAlreadyExistsException import UserAlreadyExistsException
from components.users.infrastructure.repository.core.IUserRepository import IUserRepository
from components.users.infrastructure.services.core.IUserService import IUserService
from components.users.web.models.request.UserCreateRequest import UserCreateRequest
from components.users.web.models.request.UserUpdateRequest import UserUpdateRequest
from components.users.infrastructure.models.User import User


class UserService(IUserService):
    def __init__(
        self,
        user_repo: IUserRepository,
        auth_service: IAuthService,
    ):
        self._user_repo = user_repo
        self._auth_service = auth_service

    async def register(self, user_create: UserCreateRequest) -> User:
        if await self._user_repo.get_by_email(user_create.email):
            raise UserAlreadyExistsException("User with this email already exists")
        
        if await self._user_repo.get_by_username(user_create.username):
            raise UserAlreadyExistsException("User with this username already exists")

        hashed_password = self._auth_service.get_password_hash(user_create.password)
        user = await self._user_repo.create(user_create, hashed_password)
        return user

    async def login(self, email: str, password: str) -> User:
        user = await self._user_repo.get_by_email(email)
        if not user or not self._auth_service.verify_password(
            password, user.hashed_password
        ):
            raise InvalidCredentialsException("Incorrect email or password")
        
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self._user_repo.get_by_email(email)

    async def update(self, user: User, user_update: UserUpdateRequest) -> User:
        update_data = user_update.model_dump(exclude_unset=True)
        
        if "email" in update_data and update_data["email"] != user.email:
            if await self._user_repo.get_by_email(update_data["email"]):
                raise UserAlreadyExistsException("User with this email already exists")

        if "username" in update_data and update_data["username"] != user.username:
            if await self._user_repo.get_by_username(update_data["username"]):
                raise UserAlreadyExistsException("User with this username already exists")

        updated_user = await self._user_repo.update(user, update_data)
        return updated_user