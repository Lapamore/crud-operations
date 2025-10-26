from abc import ABC, abstractmethod
from typing import List, Optional

from components.articles.infrastructure.models.Article import Article
from components.articles.web.models.ArticleCreateRequest import ArticleCreateRequest
from components.articles.web.models.ArticleUpdateRequest import ArticleUpdateRequest
from components.users.infrastructure.models.User import User


class IArticleService(ABC):

    @abstractmethod
    async def create_article(self, article_create: ArticleCreateRequest, author: User) -> Article:
        raise NotImplementedError()

    @abstractmethod
    async def get_article_by_slug(self, slug: str) -> Optional[Article]:
        raise NotImplementedError()

    @abstractmethod
    async def get_all_articles(self) -> List[Article]:
        raise NotImplementedError()

    @abstractmethod
    async def update_article(self, slug: str, article_update: ArticleUpdateRequest, user: User) -> Article:
        raise NotImplementedError()

    @abstractmethod
    async def delete_article(self, slug: str, user: User) -> None:
        raise NotImplementedError()
