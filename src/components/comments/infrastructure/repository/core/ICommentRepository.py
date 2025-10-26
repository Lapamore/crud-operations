from abc import ABC, abstractmethod
from typing import List, Optional

from components.articles.infrastructure.models.Article import Article
from components.comments.infrastructure.models.Comment import Comment
from components.comments.web.models.request.CommentCreateRequest import CommentCreateRequest
from components.users.infrastructure.models.User import User


class ICommentRepository(ABC):
    @abstractmethod
    async def create(
        self,
        comment_create: CommentCreateRequest,
        article: Article,
        author: User
    ) -> Comment:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_article(self, article: Article) -> List[Comment]:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_by_id(self, comment_id: int) -> Optional[Comment]:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, comment: Comment) -> None:
        raise NotImplementedError()
