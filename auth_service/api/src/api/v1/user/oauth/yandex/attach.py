from http import HTTPStatus

from flasgger import SwaggerView
from flask import Response

from services.oauth.yandex import get_oauth_yandex_service
from api.v1.convert_to_response import to_response
from api.v1.schemas.error_response import ErrorResponse
from api.v1.schemas.connect_info import ConnectionInfo
from api.v1.schemas.oauth.oauth2_attach_account import OAuth2AttachAccountSchema, OAuth2AttachAccount
from api.utils import extract_jwt, extract_connect_info, extract_parameters, ParametersPosition


class AttachYandexAccountView(SwaggerView):
    decorators = [
        extract_jwt,
        extract_connect_info,
        extract_parameters(schema_type=OAuth2AttachAccountSchema, pos=ParametersPosition.QUERY, extra_params=True),
    ]
    summary = "Attach Yandex account"
    description = "Attach Yandex account to user"
    tags = ["oauth"]
    security = [{"bearerAuth": []}]
    consumes = ["application/json"]
    produces = ["application/json"]
    responses = {
        HTTPStatus.ACCEPTED.value: {
            "description": "Yandex account has been successfully attached",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": "Yandex account was already attached",
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

    def get(self, parameters: OAuth2AttachAccount, connect_info: ConnectionInfo, token: str) -> Response:
        """
        Attach Yandex account to user.
        ---
        parameters:
            - in: query
              name: code
              schema:
                type: string
                example: 123456
            - in: query
              name: state
              schema:
                type: string
                example: e00ab0e2-059e-4b59-a741-ee8ab07c7f67
        """
        answer = get_oauth_yandex_service().attach_account(parameters.to_model(connect_info, token))

        return to_response(answer, ok_status_code=HTTPStatus.ACCEPTED)
