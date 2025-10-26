from abc import ABC, abstractmethod
from typing import List, Optional

from components.articles.infrastructure.models.Article import Article
from components.articles.web.models.ArticleCreateRequest import ArticleCreateRequest
from components.articles.web.models.ArticleUpdateRequest import ArticleUpdateRequest
from components.users.infrastructure.models.User import User


class IArticleRepository(ABC):
    @abstractmethod
    async def create(self, article_create: ArticleCreateRequest, author: User) -> Article:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional[Article]:
        raise NotImplementedError()

    @abstractmethod
    async def get_all(self) -> List[Article]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, article: Article, article_update: ArticleUpdateRequest) -> Article:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, article: Article) -> None:
        raise NotImplementedError()
