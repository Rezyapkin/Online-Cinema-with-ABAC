from http import HTTPStatus

from flasgger import SwaggerView
from flask import Response

from api.v1.convert_to_response import to_response
from api.v1.schemas.error_response import ErrorResponse
from api.v1.schemas.user.sign_up import SignUpSchema, SignUp, SignUpResponseSchema
from api.utils import extract_parameters, extract_connect_info
from api.v1.schemas.auth import PASSWORD_MIN_SYMBOLS
from api.v1.schemas.connect_info import ConnectionInfo
from core.settings import get_settings
from services.user import get_user_service
from core.rate_limit import get_rate_limiter


class SignUpPostView(SwaggerView):
    decorators = [
        extract_connect_info,
        extract_parameters(schema_type=SignUpSchema),
        get_rate_limiter().limit(get_settings().rate_limit.endpoint_signup, per_method=True),
    ]
    definitions = {
        "SignUpSchema": SignUpSchema,
        "SignUpResponseSchema": SignUpResponseSchema,
    }
    consumes = ["application/json"]
    produces = ["application/json"]
    description = f"Register a new account with user email and password(longer than {PASSWORD_MIN_SYMBOLS} symbols)"
    tags = ["user"]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Registration accomplished",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/definitions/SignUpResponseSchema"},
                    "example": {
                        "email": "my@example.com",
                        "id": "124abff33",
                    },
                }
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Email already exists",
            "content": {
                "application/json": {
                    "schema": ErrorResponse,
                    "example": {"description": "email already exists"},
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

    def post(self, parameters: SignUp, connect_info: ConnectionInfo) -> Response:
        """
        Create new account
        ---
        requestBody:
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/SignUpSchema'
                    example:
                        email: example@example.com
                        password: aB123456
            required: true
        """
        answer = get_user_service().create_user(parameters.to_model(connect_info))
        return to_response(answer, SignUpResponseSchema)
