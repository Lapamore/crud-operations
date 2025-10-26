from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from infrastructure.auth.core.IAuthService import IAuthService


class AuthService(IAuthService):
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_expire_minutes: int,
    ):
        self.__secret_key = secret_key
        self.__algorithm = algorithm
        self.__access_token_expire_minutes = access_token_expire_minutes
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, subject: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=self.__access_token_expire_minutes)
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.__secret_key, algorithm=self.__algorithm)
        return encoded_jwt
    
    def get_current_user_id(self, token: str) -> Optional[int]:
        try:
            payload = jwt.decode(token, self.__secret_key, algorithms=[self.__algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return int(user_id)
        except JWTError:
            return None