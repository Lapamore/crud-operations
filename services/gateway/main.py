from dishka import make_async_container
from dotenv import load_dotenv
from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka

from components.users.infrastructure.di.UserRepoProvider import UserRepoProvider
from components.users.infrastructure.di.UserServiceProvider import UserServiceProvider
from components.users.web.WebUsersInstall import WebUsersInstall
from infrastructure.auth.di.AuthProvider import AuthProvider
from infrastructure.db.di.SessionProvider import SessionProvider


from components.articles.infrastructure.di.ArticleRepoProvider import ArticleRepoProvider
from components.articles.infrastructure.di.ArticleServiceProvider import ArticleServiceProvider
from components.articles.web.WebArticlesInstall import WebArticlesInstall

from components.comments.infrastructure.di.CommentRepoProvider import CommentRepoProvider
from components.comments.infrastructure.di.CommentServiceProvider import CommentServiceProvider
from components.comments.web.WebCommentsInstall import WebCommentsInstall


def create_app() -> FastAPI:

    load_dotenv()
    
    app = FastAPI(
        title="Blog Platform API",
        description="A simple blog platform with articles, comments, and users.",
        version="1.0.0",
    )

    container = make_async_container(
        SessionProvider(),
        AuthProvider(),
        UserRepoProvider(),
        UserServiceProvider(),
        ArticleRepoProvider(),
        ArticleServiceProvider(),
        CommentRepoProvider(),
        CommentServiceProvider()
    )

    setup_dishka(container, app)

    WebUsersInstall()(app)
    WebArticlesInstall()(app)
    WebCommentsInstall()(app)

    return app