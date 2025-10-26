from typing import List, Optional

from components.articles.exceptions.ArticleNotFoundException import ArticleNotFoundException
from components.articles.exceptions.ForbiddenException import ForbiddenException
from components.articles.infrastructure.repository.core.IArticleRepository import IArticleRepository
from components.articles.infrastructure.services.core.IArticleService import IArticleService
from components.articles.infrastructure.models.Article import Article
from components.articles.web.models.ArticleCreateRequest import ArticleCreateRequest
from components.articles.web.models.ArticleUpdateRequest import ArticleUpdateRequest
from components.users.infrastructure.models.User import User


class ArticleService(IArticleService):
    def __init__(self, article_repo: IArticleRepository):
        self._article_repo = article_repo

    async def create_article(self, article_create: ArticleCreateRequest, author: User) -> Article:
        return await self._article_repo.create(article_create, author)

    async def get_article_by_slug(self, slug: str) -> Optional[Article]:
        article = await self._article_repo.get_by_slug(slug)
        if not article:
            raise ArticleNotFoundException()
        return article

    async def get_all_articles(self) -> List[Article]:
        return await self._article_repo.get_all()

    async def update_article(self, slug: str, article_update: ArticleUpdateRequest, user: User) -> Article:
        article = await self.get_article_by_slug(slug)
        if article.author_id != user.id:
            raise ForbiddenException()
        
        return await self._article_repo.update(article, article_update)

    async def delete_article(self, slug: str, user: User) -> None:
        article = await self.get_article_by_slug(slug)
        if article.author_id != user.id:
            raise ForbiddenException()
        
        await self._article_repo.delete(article)
