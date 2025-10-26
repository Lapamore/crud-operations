from fastapi import FastAPI

from components.users.web.views.RegisterUserView import RegisterUserView
from components.users.web.views.LoginUserView import LoginUserView
from components.users.web.views.GetCurrentUserView import GetCurrentUserView
from components.users.web.views.UpdateUserView import UpdateUserView
from components.users.web.models.response.UserResponse import UserResponse
from components.users.web.models.response.TokenResponse import TokenResponse


class WebUsersInstall:


    def __call__(self, app: FastAPI):
        
        login_user_view = LoginUserView()
        register_user_view = RegisterUserView()
        get_current_user_view = GetCurrentUserView()
        update_user_view = UpdateUserView()

        app.add_api_route(
            path="/api/users",
            methods=["POST"],
            tags=["users"],
            summary="Register a new user",
            endpoint=register_user_view.__call__,
            status_code=201,
        )
        app.add_api_route(
            path="/api/users/login",
            methods=["POST"],
            tags=["users"],
            summary="Login for access token",
            response_model=TokenResponse,
            endpoint=login_user_view.__call__,
        )
        app.add_api_route(
            path="/api/user",
            methods=["GET"],
            tags=["users"],
            summary="Get current user",
            response_model=UserResponse,
            endpoint=get_current_user_view.__call__,
        )
        app.add_api_route(
            path="/api/user",
            methods=["PUT"],
            tags=["users"],
            summary="Update current user",
            response_model=UserResponse,
            endpoint=update_user_view.__call__,
        )