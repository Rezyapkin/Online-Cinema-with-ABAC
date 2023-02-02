from http import HTTPStatus

from flasgger import SwaggerView
from flask import Response

from services.user import get_user_service
from api.v1.convert_to_response import to_response
from api.v1.schemas.common_request import CommonRequest
from api.v1.schemas.connect_info import ConnectionInfo
from api.v1.schemas.error_response import ErrorResponse
from api.utils import (
    extract_jwt,
    extract_connect_info,
)
from api.v1.schemas.user.current import CurrentUserInfoResponseSchema


class UserMeView(SwaggerView):
    decorators = [
        extract_jwt,
        extract_connect_info,
    ]
    summary = "User"
    description = "Current user"
    tags = ["user"]
    security = [{"bearerAuth": []}]
    consumes = ["application/json"]
    produces = ["application/json"]
    responses = {
        HTTPStatus.OK.value: {
            "description": "User information",
            "content": {
                "application/json": {
                    "schema": CurrentUserInfoResponseSchema,
                    "example": {
                        "id": "d0cc42bd-4ea7-4a03-bb27-d1b58b59ff5c",
                        "email": "admin@admin.ru",
                        "is_active": True,
                        "is_superuser": True,
                        "oauth_accounts": [
                            {"provider": "google", "account_id": "105492344174142940714"},
                            {"provider": "yandex", "account_id": "4516543"},
                        ],
                    },
                }
            },
        },
        HTTPStatus.UNAUTHORIZED.value: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "schema": ErrorResponse,
                    "example": {"description": "Missed JWT token"},
                }
            },
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": "User not found",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY.value: {
            "description": "Wrong parameters format",
            "content": {
                "application/json": {
                    "schema": ErrorResponse,
                    "example": {"description": "Wrong parameter"},
                }
            },
        },
    }

    def get(self, token: str, connect_info: ConnectionInfo) -> Response:
        """
        Get information about current user
        ---
        """
        answer = get_user_service().get_user_me(
            CommonRequest(user_ip=str(connect_info.user_ip), user_agent=connect_info.user_agent, token=token)
        )
        return to_response(answer, CurrentUserInfoResponseSchema)
