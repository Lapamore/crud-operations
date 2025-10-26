import uvicorn
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from dishka.integrations.fastapi import setup_dishka
from dishka import make_async_container
from fastapi.openapi.utils import get_openapi


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="API с настройками для отображения кнопки авторизации",
        routes=app.routes,
    )

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    # Добавляем security scheme для OAuth2
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2": {
            "type": "oauth2",
            "flows": {
                "authorizationCode": {
                    "authorizationUrl": "http://localhost:8000/realms/DevStand/protocol/openid-connect/auth",
                    "tokenUrl": "http://localhost:8000/realms/DevStand/protocol/openid-connect/token",
                    "scopes": {}
                }
            }
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

def create_app() -> FastAPI:
    load_dotenv()

    app = FastAPI(
        swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect"
    )
    app.add_middleware(GZipMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:9080",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_auth_tools(app)

    container = make_async_container(
    )
    setup_dishka(container, app)

    WebServicesInstall()(app)
    
    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)