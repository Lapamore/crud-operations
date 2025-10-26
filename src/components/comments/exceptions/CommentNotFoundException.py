from components.comments.exceptions import CommentException


class CommentNotFoundException(CommentException):
    def __init__(self, message="Comment not found"):
        self.message = message
        super().__init__(self.message)