from dishka import Provider, provide, Scope

from components.articles.infrastructure.services.core.IArticleService import IArticleService
from components.articles.infrastructure.repository.core.IArticleRepository import IArticleRepository
from components.articles.infrastructure.services.impl.ArticleService import ArticleService


class ArticleServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_article_service(self, article_repo: IArticleRepository) -> IArticleService:
        return ArticleService(article_repo)
