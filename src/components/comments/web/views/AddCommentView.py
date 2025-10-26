from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from components.articles.exceptions.ArticleNotFoundException import ArticleNotFoundException
from components.articles.infrastructure.services.core.IArticleService import IArticleService
from components.comments.infrastructure.services.core.ICommentService import ICommentService
from components.comments.web.models.request.CommentCreateRequest import CommentCreateRequest
from components.comments.web.models.response.CommentResponse import CommentResponse
from components.users.infrastructure.models.User import User
from components.users.web.dependencies import get_current_user


class AddCommentView:
    @inject
    async def __call__(
        self,
        article_service: FromDishka[IArticleService],
        comment_service: FromDishka[ICommentService],
        slug: str,
        comment_create: CommentCreateRequest,
        author: User = Depends(get_current_user),
    ) -> JSONResponse:
        try:
            article = await article_service.get_article_by_slug(slug)
            comment = await comment_service.add_comment_to_article(
                comment_create, article, author
            )
            comment_response = CommentResponse.model_validate(comment)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"comment": comment_response.model_dump()}
            )
        except ArticleNotFoundException:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
