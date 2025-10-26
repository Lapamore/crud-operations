from components.users.exceptions.UserException import UserException


class UserNotFoundException(UserException):
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)