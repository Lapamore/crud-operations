from zope.interface import Interface


class IAuthService(Interface):
    def get_password_hash(self, password: str) -> str:
        raise NotImplementedError()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError()
    
    def create_access_token(self, subject: str) -> str:
        raise NotImplementedError()