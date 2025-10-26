from fastapi import FastAPI
from typing import List

from components.articles.web.models.ArticleResponse import ArticleResponse
from components.articles.web.views.CreateArticleView import CreateArticleView
from components.articles.web.views.DeleteArticleView import DeleteArticleView
from components.articles.web.views.GetArticleBySlugView import GetArticleBySlugView
from components.articles.web.views.GetArticleView import GetArticleView
from components.articles.web.views.UpdateArticleView import UpdateArticleView


class WebArticlesInstall:

    def __call__(self, app: FastAPI):
        
        create_article_view = CreateArticleView()
        delete_article_view = DeleteArticleView()
        get_article_by_slug_view = GetArticleBySlugView()
        get_articles_view = GetArticleView()
        update_article_view = UpdateArticleView()

        app.add_api_route(
            path="/api/articles",
            methods=["POST"],
            tags=["articles"],
            summary="Create a new article",
            endpoint=create_article_view.__call__,
            status_code=201,
        )
        app.add_api_route(
            path="/api/articles",
            methods=["GET"],
            tags=["articles"],
            summary="Get all articles",
            response_model=List[ArticleResponse],
            endpoint=get_articles_view.__call__,
        )
        app.add_api_route(
            path="/api/articles/{slug}",
            methods=["GET"],
            tags=["articles"],
            summary="Get article by slug",
            response_model=ArticleResponse,
            endpoint=get_article_by_slug_view.__call__,
        )
        app.add_api_route(
            path="/api/articles/{slug}",
            methods=["PUT"],
            tags=["articles"],
            summary="Update article by slug",
            response_model=ArticleResponse,
            endpoint=update_article_view.__call__,
        )
        app.add_api_route(
            path="/api/articles/{slug}",
            methods=["DELETE"],
            tags=["articles"],
            summary="Delete article by slug",
            endpoint=delete_article_view.__call__,
            status_code=204,
        )
