from http import HTTPStatus

from flasgger import SwaggerView
from flask import Response

from api.v1.schemas.auth.token import Token
from api.utils import extract_jwt, extract_connect_info
from api.v1.convert_to_response import to_response
from api.v1.schemas.error_response import ErrorResponse
from models.common_request import CommonRequest
from services.auth import get_auth_service
from api.v1.schemas.connect_info import ConnectionInfo


class RefreshPostView(SwaggerView):
    decorators = [
        extract_jwt,
        extract_connect_info,
    ]
    consumes = ["application/json"]
    produces = ["application/json"]
    security = [{"bearerAuth": []}]
    summary = "Update tokens"
    description = "Create Access and Refresh token by valid Refresh token"
    tags = ["auth"]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Password changed, devices logged out",
            "content": {
                "application/json": {
                    "schema": Token,
                    "example": {
                        "access_token": "access_token",
                        "refresh_token": "refresh_token",
                        "token_type": "Bearer",
                        "access_token_lifetime_minutes": 100,
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
    }

    def post(self, token: str, connect_info: ConnectionInfo) -> Response:
        answer = get_auth_service().refresh_token(
            CommonRequest(
                user_ip=str(connect_info.user_ip),
                user_agent=connect_info.user_agent,
                token=token,
            )
        )
        return to_response(answer, Token)
