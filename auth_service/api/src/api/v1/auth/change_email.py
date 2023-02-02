from http import HTTPStatus

from flasgger import SwaggerView
from flask import Response

from api.v1.convert_to_response import to_response
from api.v1.schemas.auth.email import ChangeEmailSchema, NewEmail
from api.utils import extract_jwt, extract_parameters, extract_connect_info
from api.v1.schemas.connect_info import ConnectionInfo
from api.v1.schemas.error_response import ErrorResponse
from services.auth import get_auth_service


class NewEmailPostView(SwaggerView):
    decorators = [
        extract_jwt,
        extract_connect_info,
        extract_parameters(schema_type=ChangeEmailSchema),
    ]
    definitions = {"ChangeEmailSchema": ChangeEmailSchema}
    consumes = ["application/json"]
    produces = ["application/json"]
    description = "Change account email"
    tags = ["auth"]
    security = [{"bearerAuth": []}]
    responses = {
        HTTPStatus.NO_CONTENT.value: {"description": "Email changed"},
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Wrong parameter",
            "content": {
                "application/json": {
                    "schema": ErrorResponse,
                    "example": {"description": "email already exists"},
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

    def post(self, token: str, connect_info: ConnectionInfo, parameters: NewEmail) -> Response:
        """
        Change email
        ---
        requestBody:
           content:
               application/json:
                   schema:
                       $ref: '#/definitions/ChangeEmailSchema'
                   example:
                       password: 'aB12345'
                       new_email: 'my@example.com'
           required: true
        """
        result = get_auth_service().change_email(parameters.to_model(connect_info, token))
        return to_response(result)
