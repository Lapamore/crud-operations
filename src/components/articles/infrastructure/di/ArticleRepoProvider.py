from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from components.articles.infrastructure.repository.core.IArticleRepository import IArticleRepository
from components.articles.infrastructure.repository.impl.ArticleRepository import ArticleRepository


class ArticleRepoProvider(Provider):
    @provide(scope=Scope.APP)
    def get_article_repo(self, session: AsyncSession) -> IArticleRepository:
        return ArticleRepository(session)
