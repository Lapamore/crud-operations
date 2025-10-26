from components.articles.exceptions.ArticleException import ArticleException


class ArticleNotFoundException(ArticleException):
    def __init__(self, message="Article not found"):
        self.message = message
        super().__init__(self.message)