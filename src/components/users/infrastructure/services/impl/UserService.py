from typing import Optional
from zope.interface import implementer

from infrastructure.auth.core.IAuthService import IAuthService
from components.users.exceptions.InvalidCredentialsException import InvalidCredentialsException
from components.users.exceptions.UserAlreadyExistsException import UserAlreadyExistsException
from components.users.exceptions.UserNotFoundException import UserNotFoundException
from components.users.infrastructure.repository.core.IUserRepository import IUserRepository
from components.users.infrastructure.services.core.IUserService import IUserService
from components.users.web.models.request.UserCreateRequest import UserCreateRequest
from components.users.web.models.request.UserUpdateRequest import UserUpdateRequest
from components.users.web.models.response.UserResponse import UserResponse



@implementer(IUserService)
class UserService:
    def __init__(self, 
                 user_repo: IUserRepository,
                 user_mapper: ...,
                 auth_service: IAuthService):
        self._user_repo = user_repo
        self._user_mapper = user_mapper
        self._auth_service = auth_service

    async def register_user(self, user_create: UserCreateRequest) -> UserResponse:
        existing_user = await self._user_repo.get_by_email(user_create.email)
        if existing_user:
            raise UserAlreadyExistsException("User with this email already exists")
        
        existing_user = await self._user_repo.get_by_username(user_create.username)
        if existing_user:
            raise UserAlreadyExistsException("User with this username already exists")

        hashed_password = self._auth_service.get_password_hash(user_create.password)
        user = await self._user_mapper.create({
            "email": user_create.email,
            "username": user_create.username,
            "hashed_password": hashed_password
        })
        return UserResponse.model_validate(user)

    async def login_user(self, email: str, password: str) -> str:
        user = await self._user_repo.get_by_email(email)
        is_corrected_pass = self._auth_service.verify_password(password, user.hashed_password)
        if not user or not is_corrected_pass:
            raise InvalidCredentialsException("Incorrect email or password")
        
        access_token = self._auth_service.create_access_token(data={"sub": user.email})
        return access_token

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        user = await self._user_repo.get_by_email(email)
        if not user:
            return None
        return UserResponse.model_validate(user)

    async def update_user(self, current_email: str, user_update: UserUpdateRequest) -> UserResponse:
        current_user = await self._user_repo.get_by_email(current_email)
        if not current_user:
            raise UserNotFoundException()
        
        update_data = user_update.model_dump(exclude_unset=True)
        
        updated_user = await self._user_mapper.update(current_user, update_data)
        return UserResponse.model_validate(updated_user)