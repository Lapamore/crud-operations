from dishka import Provider, provide, Scope

from components.comments.infrastructure.repository.core.ICommentRepository import ICommentRepository
from components.comments.infrastructure.services.core.ICommentService import ICommentService
from components.comments.infrastructure.services.impl.CommentService import CommentService


class CommentServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_comment_service(self, comment_repo: ICommentRepository) -> ICommentService:
        return CommentService(comment_repo)
