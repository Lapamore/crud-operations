from typing import List, Optional
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from components.articles.infrastructure.repository.core.IArticleRepository import IArticleRepository
from components.articles.infrastructure.models.Article import Article
from components.articles.web.models.ArticleCreateRequest import ArticleCreateRequest
from components.articles.web.models.ArticleUpdateRequest import ArticleUpdateRequest
from components.users.infrastructure.models.User import User


class ArticleRepository(IArticleRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, article_create: ArticleCreateRequest, author: User) -> Article:
        slug = slugify(article_create.title)
        
        while await self.get_by_slug(slug):
            slug = f"{slug}-1"

        article = Article(
            **article_create.model_dump(exclude={"tagList"}),
            slug=slug,
            author_id=author.id,
        )
        self._session.add(article)
        await self._session.commit()
        await self._session.refresh(article)
        return article

    async def get_by_slug(self, slug: str) -> Optional[Article]:
        query = select(Article).where(Article.slug == slug).options(selectinload(Article.author))
        result = await self._session.execute(query)
        return result.scalars().one_or_none()

    async def get_all(self) -> List[Article]:
        query = select(Article).options(selectinload(Article.author))
        result = await self._session.execute(query)
        return result.scalars().all()

    async def update(self, article: Article, article_update: ArticleUpdateRequest) -> Article:
        update_data = article_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(article, key, value)
        
        if "title" in update_data:
            article.slug = slugify(update_data["title"])
        
        await self._session.commit()
        await self._session.refresh(article)
        return article

    async def delete(self, article: Article) -> None:
        await self._session.delete(article)
        await self._session.commit()
