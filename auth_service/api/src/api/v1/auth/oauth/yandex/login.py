from http import HTTPStatus

from flasgger import SwaggerView
from flask import Response

from api.v1.convert_to_response import to_response
from api.v1.schemas.oauth.oauth2_login import OAuth2LogInSchema, OAuth2LogIn
from api.v1.schemas.auth.token import Token
from api.utils import extract_parameters, extract_connect_info, ParametersPosition
from api.v1.schemas.error_response import ErrorResponse
from services.oauth.yandex import get_oauth_yandex_service
from api.v1.schemas.connect_info import ConnectionInfo


class YandexOAuthLogInView(SwaggerView):
    decorators = [
        extract_connect_info,
        extract_parameters(schema_type=OAuth2LogInSchema, pos=ParametersPosition.QUERY),
    ]
    consumes = ["application/json"]
    produces = ["application/json"]
    description = "Logging wia Yandex account"
    tags = ["oauth"]
    definitions = {"OAuth2LogInSchema": OAuth2LogInSchema}
    responses = {
        HTTPStatus.OK.value: {
            "description": "Account entered",
            "content": {
                "application/json": {
                    "schema": Token,
                    "example": {
                        "access_token": "access_token",
                        "expires_in": 100,
                        "refresh_token": "refresh_token",
                        "token_type": "Bearer",
                    },
                }
            },
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
        HTTPStatus.UNPROCESSABLE_ENTITY.value: {
            "description": "Wrong parameters format",
            "content": {
                "application/json": {
                    "schema": ErrorResponse,
                    "example": {"description": "Wrong format"},
                }
            },
        },
    }

    def get(self, parameters: OAuth2LogIn, connect_info: ConnectionInfo) -> Response:
        """
        Log into account wia Yandex account
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

        answer = get_oauth_yandex_service().login(parameters.to_model(connect_info))
        return to_response(answer, Token)
