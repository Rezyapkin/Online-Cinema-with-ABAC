from http import HTTPStatus

from flasgger import SwaggerView
from flask import Response

from services.oauth.google import get_oauth_google_service
from api.v1.convert_to_response import to_response
from api.v1.schemas.error_response import ErrorResponse
from api.v1.schemas.connect_info import ConnectionInfo
from api.v1.schemas.oauth.oauth2_attach_account import OAuth2AttachAccountSchema, OAuth2AttachAccount
from api.utils import extract_jwt, extract_connect_info, extract_parameters, ParametersPosition


class AttachGoogleAccountView(SwaggerView):
    decorators = [
        extract_jwt,
        extract_connect_info,
        extract_parameters(schema_type=OAuth2AttachAccountSchema, pos=ParametersPosition.QUERY, extra_params=True),
    ]
    summary = "Attach Google account"
    description = "Attach Google account to user"
    tags = ["oauth"]
    security = [{"bearerAuth": []}]
    consumes = ["application/json"]
    produces = ["application/json"]
    responses = {
        HTTPStatus.ACCEPTED.value: {
            "description": "Google account has been successfully attached",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": "Google account was already attached",
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
        Attach Google account to user.
        ---
        parameters:
            - in: query
              name: code
              schema:
                type: string
                example: 4/F0AWtgzh6n6Xx6p3Who6eQCuOxEzK0As_2kgmsI3De_zJ8nSAAEU5z0Oymi9PwjYfwQCRv8w
            - in: query
              name: state
              schema:
                type: string
                example: e00ab0e2-059e-4b59-a741-ee8ab07c7f67
        """
        answer = get_oauth_google_service().attach_account(parameters.to_model(connect_info, token))

        return to_response(answer, ok_status_code=HTTPStatus.ACCEPTED)
