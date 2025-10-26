from typing import List
from fastapi import HTTPException, status
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from components.articles.exceptions.ArticleNotFoundException import ArticleNotFoundException
from components.articles.infrastructure.services.core.IArticleService import IArticleService
from components.comments.infrastructure.services.core.ICommentService import ICommentService
from components.comments.web.models.response.CommentResponse import CommentResponse



class GetCommentsView:
    @inject
    async def __call__(
        slug: str,
        article_service: FromDishka[IArticleService],
        comment_service: FromDishka[ICommentService],
    ) -> List[CommentResponse]:
        try:
            article = await article_service.get_article_by_slug(slug)
            comments = await comment_service.get_comments_for_article(article)
            return [CommentResponse.model_validate(comment) for comment in comments]
        except ArticleNotFoundException:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
