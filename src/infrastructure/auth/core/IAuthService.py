from abc import ABC, abstractmethod


class IAuthService(ABC):
    @abstractmethod
    def get_password_hash(self, password: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError()
    
    @abstractmethod
    def create_access_token(self, subject: str) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    def get_current_user_id(self, token: str) -> int:
        raise NotImplementedError()