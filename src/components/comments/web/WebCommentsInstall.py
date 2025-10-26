from fastapi import FastAPI
from typing import List

from components.comments.web.models.response.CommentResponse import CommentResponse
from components.comments.web.views.AddCommentView import AddCommentView
from components.comments.web.views.DeleteCommentView import DeleteCommentView
from components.comments.web.views.GetCommentsView import GetCommentsView


class WebCommentsInstall:
    def __call__(self, app: FastAPI):
        add_comment_view = AddCommentView()
        delete_comment_view = DeleteCommentView()
        git_comments_view = GetCommentsView()

        app.add_api_route(
            path="/api/articles/{slug}/comments",
            methods=["POST"],
            tags=["comments"],
            summary="Add a comment to an article",
            endpoint=add_comment_view.__call__,
            status_code=201,
        )
        app.add_api_route(
            path="/api/articles/{slug}/comments",
            methods=["GET"],
            tags=["comments"],
            summary="Get comments for an article",
            response_model=List[CommentResponse],
            endpoint=git_comments_view.__call__,
        )
        app.add_api_route(
            path="/api/articles/{slug}/comments/{comment_id}",
            methods=["DELETE"],
            tags=["comments"],
            summary="Delete a comment",
            endpoint=delete_comment_view.__call__,
            status_code=204,
        )
