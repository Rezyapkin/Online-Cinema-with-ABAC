from http import HTTPStatus

from flasgger import SwaggerView
from flask import Response

from api.v1.convert_to_response import to_response
from api.v1.schemas.auth.password import (
    ChangePasswordSchema,
    Password,
)
from api.v1.schemas.auth import PASSWORD_MIN_SYMBOLS
from api.utils import extract_jwt, extract_parameters, extract_connect_info
from api.v1.schemas.connect_info import ConnectionInfo
from api.v1.schemas.error_response import ErrorResponse
from services.auth import get_auth_service


class NewPasswordPostView(SwaggerView):
    decorators = [
        extract_jwt,
        extract_connect_info,
        extract_parameters(schema_type=ChangePasswordSchema),
    ]
    definitions = {"ChangePasswordSchema": ChangePasswordSchema}
    consumes = ["application/json"]
    produces = ["application/json"]
    tags = ["auth"]
    description = f"Change account password. Required minimum {PASSWORD_MIN_SYMBOLS} symbols"
    security = [{"bearerAuth": []}]
    responses = {
        HTTPStatus.NO_CONTENT.value: {"description": "Password changed"},
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
                    "example": {
                        "description": f"Password length should be bigger than {PASSWORD_MIN_SYMBOLS} symbols."
                    },
                }
            },
        },
    }

    def post(self, token: str, connect_info: ConnectionInfo, parameters: Password) -> Response:
        """
        Change password
        ---
        requestBody:
           content:
               application/json:
                   schema:
                       $ref: '#/definitions/ChangePasswordSchema'
                   example:
                       old_password: 'aB12345'
                       new_password: '54321Ba'
                       new_password_confirm: '54321Ba'
           required: true
        """
        result = get_auth_service().change_password(parameters.to_model(connect_info, token))
        return to_response(result)
