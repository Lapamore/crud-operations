from fastapi import Depends, HTTPException, status, Response
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from components.articles.exceptions.ForbiddenException import ForbiddenException
from components.comments.exceptions.CommentNotFoundException import CommentNotFoundException
from components.comments.infrastructure.services.core.ICommentService import ICommentService
from components.users.infrastructure.models.User import User
from components.users.web.dependencies import get_current_user


class DeleteCommentView:
    @inject
    async def __call__(
        self,
        comment_service: FromDishka[ICommentService],
        comment_id: int,
        user: User = Depends(get_current_user)
    ) -> Response:
        try:
            await comment_service.delete_comment(comment_id, user)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except CommentNotFoundException:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        except ForbiddenException:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the author of this comment")
