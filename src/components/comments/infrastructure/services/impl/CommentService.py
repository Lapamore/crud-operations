from typing import List

from components.articles.exceptions.ForbiddenException import ForbiddenException
from components.articles.infrastructure.models.Article import Article
from components.comments.exceptions.CommentNotFoundException import CommentNotFoundException
from components.comments.infrastructure.models.Comment import Comment
from components.comments.infrastructure.repository.core.ICommentRepository import ICommentRepository
from components.comments.infrastructure.services.core.ICommentService import ICommentService
from components.comments.web.models.request.CommentCreateRequest import CommentCreateRequest
from components.users.infrastructure.models.User import User


class CommentService(ICommentService):
    def __init__(self, comment_repo: ICommentRepository):
        self._comment_repo = comment_repo

    async def add_comment_to_article(
        self,
        comment_create: CommentCreateRequest,
        article: Article,
        author: User,
    ) -> Comment:
        return await self._comment_repo.create(comment_create, article, author)

    async def get_comments_for_article(self, article: Article) -> List[Comment]:
        return await self._comment_repo.get_by_article(article)

    async def delete_comment(self, comment_id: int, user: User) -> None:
        comment = await self._comment_repo.get_by_id(comment_id)
        if not comment:
            raise CommentNotFoundException()

        if comment.author_id != user.id:
            raise ForbiddenException()

        await self._comment_repo.delete(comment)
