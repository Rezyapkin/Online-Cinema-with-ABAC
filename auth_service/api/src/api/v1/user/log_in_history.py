from http import HTTPStatus

from flasgger import SwaggerView
from flask import Response

from api.v1.convert_to_response import to_response
from api.v1.schemas.error_response import ErrorResponse
from api.v1.schemas.user.log_in_history import LogInHistoryResponseSchema
from api.utils import (
    extract_jwt,
    extract_connect_info,
    extract_parameters,
    ParametersPosition,
)
from api.v1.schemas.connect_info import ConnectionInfo
from api.v1.schemas.user.log_in_history import (
    LogInHistoryRequestSchema,
    LogInHistoryRequest,
)
from services.user import get_user_service


class LogInHistoryGetView(SwaggerView):
    decorators = [
        extract_jwt,
        extract_connect_info,
        extract_parameters(schema_type=LogInHistoryRequestSchema, pos=ParametersPosition.QUERY),
    ]
    summary = "Log in history"
    description = "Account log in history for last entries"
    definitions = {"LogInHistoryRequestSchema": LogInHistoryRequestSchema}
    tags = ["user"]
    security = [{"bearerAuth": []}]
    consumes = ["application/json"]
    produces = ["application/json"]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Success",
            "content": {
                "application/json": {
                    "schema": LogInHistoryResponseSchema,
                    "example": {
                        "data": [
                            {
                                "date_time": "2023-01-06T10:20:45.270Z",
                                "user_agent": "Unknown",
                                "user_ip": "192.168.0.2",
                                "device": "web",
                            },
                            {
                                "date_time": "2023-01-06T10:30:55.270Z",
                                "user_agent": "Unknown",
                                "user_ip": "192.168.0.3",
                                "device": "mobile",
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
        HTTPStatus.UNPROCESSABLE_ENTITY.value: {
            "description": "Wrong parameters format",
            "content": {
                "application/json": {
                    "schema": ErrorResponse,
                    "example": {"description": "Wrong offset"},
                }
            },
        },
    }

    def get(self, parameters: LogInHistoryRequest, connect_info: ConnectionInfo, token: str) -> Response:
        """
        Log in history
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

        answer = get_user_service().get_log_in_history(parameters.to_model(connect_info, token))
        return to_response(answer)
