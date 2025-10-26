from abc import ABC, abstractmethod
from typing import List

from components.articles.infrastructure.models.Article import Article
from components.comments.infrastructure.models.Comment import Comment
from components.comments.web.models.request.CommentCreateRequest import CommentCreateRequest
from components.users.infrastructure.models.User import User


class ICommentService(ABC):
    @abstractmethod
    async def add_comment_to_article(
        self,
        comment_create: CommentCreateRequest,
        article: Article,
        author: User,
    ) -> Comment:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_comments_for_article(self, article: Article) -> List[Comment]:
        raise NotImplementedError()
    
    @abstractmethod
    async def delete_comment(self, comment_id: int, user: User) -> None:
        raise NotImplementedError()