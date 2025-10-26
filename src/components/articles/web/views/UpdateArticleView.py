from fastapi import Depends, HTTPException, status
from dishka import FromDishka

from dishka.integrations.fastapi import inject
from components.articles.exceptions.ArticleNotFoundException import ArticleNotFoundException
from components.articles.exceptions.ForbiddenException import ForbiddenException
from components.articles.infrastructure.services.core.IArticleService import IArticleService
from components.articles.web.models.ArticleUpdateRequest import ArticleUpdateRequest
from components.articles.web.models.ArticleResponse import ArticleResponse
from components.users.infrastructure.models.User import User
from components.users.web.dependencies import get_current_user


class UpdateArticleView:
    @inject
    async def __call__(
        self,
        article_service: FromDishka[IArticleService],
        slug: str,
        article_update: ArticleUpdateRequest,
        user: User = Depends(get_current_user),
    ) -> ArticleResponse:
        try:
            article = await article_service.update_article(slug, article_update, user)
            return ArticleResponse.model_validate(article)
        except ArticleNotFoundException:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
        except ForbiddenException:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the author of this article")
