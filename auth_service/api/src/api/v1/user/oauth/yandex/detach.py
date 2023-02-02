from http import HTTPStatus

from flasgger import SwaggerView
from flask import Response

from services.oauth.yandex import get_oauth_yandex_service
from api.v1.convert_to_response import to_response
from api.v1.schemas.error_response import ErrorResponse
from api.v1.schemas.connect_info import ConnectionInfo
from api.v1.schemas.common_request import CommonRequest
from api.utils import extract_jwt, extract_connect_info


class DetachYandexAccountView(SwaggerView):
    decorators = [
        extract_jwt,
        extract_connect_info,
    ]
    summary = "Detach Yandex account"
    description = "Detach Yandex account from user"
    tags = ["oauth"]
    security = [{"bearerAuth": []}]
    consumes = ["application/json"]
    produces = ["application/json"]
    responses = {
        HTTPStatus.NO_CONTENT.value: {
            "description": "Yandex account has been successfully detached",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": "Yandex account was not attached",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Internal error",
            "content": {
                "application/json": {
                    "schema": ErrorResponse,
                    "example": {"description": "Incorrect response from the OAuth-provider!"},
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

    def delete(self, token: str, connect_info: ConnectionInfo) -> Response:
        """
        Detach Yandex account from user.
        ---
        """
        answer = get_oauth_yandex_service().detach_account(
            CommonRequest(
                user_ip=str(connect_info.user_ip),
                user_agent=connect_info.user_agent,
                token=token,
            )
        )

        return to_response(answer)
