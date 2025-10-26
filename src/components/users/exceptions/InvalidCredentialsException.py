from components.users.exceptions.UserException import UserException


class InvalidCredentialsException(UserException):
    def __init__(self, message="Incorrect email or password"):
        self.message = message
        super().__init__(self.message)