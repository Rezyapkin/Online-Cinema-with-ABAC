from http import HTTPStatus

from flasgger import SwaggerView
from flask import Response

from api.v1.convert_to_response import to_response
from api.v1.schemas.auth.log_in import LogInSchema, LogIn
from api.v1.schemas.auth.token import Token
from api.utils import extract_parameters, extract_connect_info
from api.v1.schemas.error_response import ErrorResponse
from services.auth import get_auth_service
from api.v1.schemas.connect_info import ConnectionInfo


class LogInPostView(SwaggerView):
    decorators = [
        extract_connect_info,
        extract_parameters(schema_type=LogInSchema),
    ]
    consumes = ["application/json"]
    produces = ["application/json"]
    description = "Logging with user email and password"
    tags = ["auth"]
    definitions = {"LogInSchema": LogInSchema}
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
            "description": "Access denied",
            "content": {
                "application/json": {
                    "schema": ErrorResponse,
                    "example": {"description": "Wrong password"},
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
                    "example": {"description": "Wrong format: email"},
                }
            },
        },
    }

    def post(self, parameters: LogIn, connect_info: ConnectionInfo) -> Response:
        """
        Log into account with email
        ---
        requestBody:
           content:
               application/json:
                   schema:
                       $ref: '#/definitions/LogInSchema'
                   example:
                       email: example@example.com
                       password: aB123456
           required: true
        """

        answer = get_auth_service().log_in(parameters.to_model(connect_info))
        return to_response(answer, Token)
