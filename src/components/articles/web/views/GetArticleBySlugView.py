from fastapi import HTTPException, status
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from components.articles.exceptions.ArticleNotFoundException import ArticleNotFoundException
from components.articles.infrastructure.services.core.IArticleService import IArticleService
from components.articles.web.models.ArticleResponse import ArticleResponse


class GetArticleBySlugView:
    @inject
    async def __call__(
            self,
            slug: str,
            article_service: FromDishka[IArticleService]
    ) -> ArticleResponse:
        try:
            article = await article_service.get_article_by_slug(slug)
            return ArticleResponse.model_validate(article)
        except ArticleNotFoundException:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

