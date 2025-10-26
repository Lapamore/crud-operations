from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from components.articles.infrastructure.models.Article import Article
from components.comments.infrastructure.repository.core.ICommentRepository import ICommentRepository
from components.comments.infrastructure.models.Comment import Comment
from components.comments.web.models.request.CommentCreateRequest import CommentCreateRequest
from components.users.infrastructure.models.User import User


class CommentRepository(ICommentRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        comment_create: CommentCreateRequest,
        article: Article,
        author: User
    ) -> Comment:
        comment = Comment(
            body=comment_create.body,
            article_id=article.id,
            author_id=author.id,
        )
        self._session.add(comment)
        await self._session.commit()
        await self._session.refresh(comment)
        return comment

    async def get_by_article(self, article: Article) -> List[Comment]:
        query = select(Comment).where(Comment.article_id == article.id).options(selectinload(Comment.author))
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, comment_id: int) -> Optional[Comment]:
        query = select(Comment).where(Comment.id == comment_id).options(selectinload(Comment.author))
        result = await self._session.execute(query)
        return result.scalars().one_or_none()

    async def delete(self, comment: Comment) -> None:
        await self._session.delete(comment)
        await self._session.commit()
