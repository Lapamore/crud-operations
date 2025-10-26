from fastapi import Depends, HTTPException, status, Response
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from components.articles.exceptions import ArticleNotFoundException, ForbiddenException
from components.articles.infrastructure.services.core import IArticleService
from components.users.infrastructure.models import User



class DeleteArticleView:
    @inject
    async def __call__(
        slug: str,
        article_service: FromDishka[IArticleService] = None,
        user: User = Depends(get_current_user),
    ) -> Response:
        try:
            await article_service.delete_article(slug, user)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except ArticleNotFoundException:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
        except ForbiddenException:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the author of this article")
