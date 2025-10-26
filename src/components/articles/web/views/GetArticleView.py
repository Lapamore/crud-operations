
from typing import List
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from components.articles.infrastructure.services.core.IArticleService import IArticleService
from components.articles.web.models.ArticleResponse import ArticleResponse


class GetArticleView:
    @inject
    async def __call__(
            self,
            article_service: FromDishka[IArticleService]
    ) -> List[ArticleResponse]:
        articles = await article_service.get_all_articles()
        return [ArticleResponse.model_validate(article) for article in articles]