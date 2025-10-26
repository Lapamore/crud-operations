from fastapi import Depends, status
from fastapi.responses import JSONResponse
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from components.articles.infrastructure.services.core.IArticleService import IArticleService

from components.articles.web.models.ArticleCreateRequest import ArticleCreateRequest
from components.articles.web.models.ArticleResponse import ArticleResponse
from components.users.infrastructure.models.User import User
from components.users.web.dependencies import get_current_user


class CreateArticleView:
    @inject
    async def __call__(
            self,
            article_create_request: ArticleCreateRequest,
            article_service: FromDishka[IArticleService],
            author: User = Depends(get_current_user)
    ) -> JSONResponse:
        article = await article_service.create_article(article_create_request, author)
        article_response = ArticleResponse.model_validate(article)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"article": article_response.model_dump()}
        )
