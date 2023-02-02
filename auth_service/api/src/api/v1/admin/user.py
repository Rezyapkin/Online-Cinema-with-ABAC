from http import HTTPStatus

from flasgger import SwaggerView
from flask import Response

from api.v1.convert_to_response import to_response
from api.v1.schemas.admin.user import (
    UserInfoSchema,
    UserInfoListSchema,
    UserListRequestSchema,
    UserRequestSchema,
    UserListRequest,
)
from api.v1.schemas.connect_info import ConnectionInfo
from api.v1.schemas.error_response import ErrorResponse
from api.utils import (
    extract_jwt,
    extract_connect_info,
    extract_parameters,
    ParametersPosition,
)
from services.admin import get_admin_service


class UserView(SwaggerView):
    decorators = [
        extract_jwt,
        extract_connect_info,
    ]
    summary = "User"
    tags = ["admin"]
    security = [{"bearerAuth": []}]
    consumes = ["application/json"]
    produces = ["application/json"]
    responses = {
        HTTPStatus.OK.value: {
            "description": "User information",
            "content": {
                "application/json": {
                    "schema": UserInfoSchema,
                    "example": {
                        "id": "d0cc42bd-4ea7-4a03-bb27-d1b58b59ff5c",
                        "email": "admin@admin.ru",
                        "is_active": True,
                        "is_superuser": True,
                        "oauth_accounts": [
                            {"provider": "google", "account_id": "105492344174142940714"},
                            {"provider": "yandex", "account_id": "4516543"},
                        ],
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
        HTTPStatus.FORBIDDEN.value: {
            "description": "Forbidden",
            "content": {
                "application/json": {
                    "schema": ErrorResponse,
                    "example": {"description": "Permission denied"},
                }
            },
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": "User not found",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY.value: {
            "description": "Wrong parameters format",
            "content": {
                "application/json": {
                    "schema": ErrorResponse,
                    "example": {"description": "Wrong parameter"},
                }
            },
        },
    }

    def get(self, token: str, connect_info: ConnectionInfo, id: str) -> Response:
        """
        Get user information by `id`
        ---
        parameters:
            - in: path
              name: id
              schema:
                type: string
                example: d0cc42bd-4ea7-4a03-bb27-d1b58b59ff5c
        """
        answer = get_admin_service().get_user(UserRequestSchema().load({"id": id}).to_model(connect_info, token))
        return to_response(answer, UserInfoSchema)


class UserListView(SwaggerView):
    decorators = [
        extract_jwt,
        extract_connect_info,
        extract_parameters(schema_type=UserListRequestSchema, pos=ParametersPosition.QUERY),
    ]
    summary = "User"
    tags = ["admin"]
    security = [{"bearerAuth": []}]
    consumes = ["application/json"]
    produces = ["application/json"]
    responses = {
        HTTPStatus.OK.value: {
            "description": "List of users",
            "content": {
                "application/json": {
                    "schema": UserInfoListSchema,
                    "example": {
                        "users": [
                            {
                                "id": "d0cc42bd-4ea7-4a03-bb27-d1b58b59ff5c",
                                "email": "admin@admin.ru",
                                "is_active": True,
                                "is_superuser": True,
                            },
                            {
                                "id": "7a1d9a43-bf6a-4e8d-a20e-709e83fe8eb1",
                                "email": "test@test.ru",
                                "is_active": True,
                                "is_superuser": False,
                            },
                        ],
                        "pagination": {"total_count": 20, "total_pages": 2, "next_page": 2},
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
        HTTPStatus.FORBIDDEN.value: {
            "description": "Forbidden",
            "content": {
                "application/json": {
                    "schema": ErrorResponse,
                    "example": {"description": "Permission denied"},
                }
            },
        },
        HTTPStatus.UNPROCESSABLE_ENTITY.value: {
            "description": "Wrong parameters format",
            "content": {
                "application/json": {
                    "schema": ErrorResponse,
                    "example": {"description": "Wrong parameter"},
                }
            },
        },
    }

    def get(self, token: str, connect_info: ConnectionInfo, parameters: UserListRequest) -> Response:
        """
        Get list of users
        ---
        parameters:
            - in: query
              name: page_number
              schema:
                type: integer
                example: 1
            - in: query
              name: page_size
              schema:
                type: integer
                example: 10
        """

        answer = get_admin_service().get_user_list(parameters.to_model(connect_info, token))
        return to_response(answer)
