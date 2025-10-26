from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from components.comments.infrastructure.repository.core.ICommentRepository import ICommentRepository
from components.comments.infrastructure.repository.impl.CommentRepository import CommentRepository


class CommentRepoProvider(Provider):
    @provide(scope=Scope.APP)
    def get_comment_repo(self, session: AsyncSession) -> ICommentRepository:
        return CommentRepository(session)
