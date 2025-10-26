from components.articles.exceptions.ArticleException import ArticleException


class ForbiddenException(ArticleException):
    def __init__(self, message="Forbidden"):
        self.message = message
        super().__init__(self.message)