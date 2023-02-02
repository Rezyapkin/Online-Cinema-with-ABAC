from http import HTTPStatus

import flask
from flasgger import SwaggerView

from api.v1.convert_to_response import to_response
from api.v1.schemas.error_response import ErrorResponse
from api.utils import extract_jwt, extract_connect_info
from api.v1.schemas.connect_info import ConnectionInfo
from models.common_request import CommonRequest
from services.auth import get_auth_service


class LogOutPostView(SwaggerView):
    decorators = [
        extract_jwt,
        extract_connect_info,
    ]
    consumes = ["application/json"]
    produces = ["application/json"]
    summary = "Log out"
    description = "Log out from account"
    security = [{"bearerAuth": []}]
    tags = ["auth"]
    responses = {
        HTTPStatus.NO_CONTENT.value: {
            "description": "Success",
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

    def post(
        self,
        token: str,
        connect_info: ConnectionInfo,
    ) -> flask.Response:
        result = get_auth_service().log_out(
            CommonRequest(
                user_ip=str(connect_info.user_ip),
                user_agent=connect_info.user_agent,
                token=token,
            )
        )
        return to_response(result)
