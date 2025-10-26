from components.users.exceptions.UserException import UserException


class UserAlreadyExistsException(UserException):
    def __init__(self, message="User with this email or username already exists"):
        self.message = message
        super().__init__(self.message)