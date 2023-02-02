from http import HTTPStatus
from typing import Any

from flask import Response, jsonify
from flasgger import Schema

from models.status import Status, StatusCode
from models.user import UserListResponse
from models.policy import PolicyListResponse
from models.log_in_history import LogInHistoryResponse
from api.v1.schemas.error_response import ErrorResponse
from api.v1.schemas.user.log_in_history import LogInHistoryResponseSchema
from api.v1.schemas.admin.user import UserInfoListSchema
from api.v1.schemas.admin.policy import PolicyListSchema


def status_to_response(status: Status, ok_status: HTTPStatus = HTTPStatus.NO_CONTENT) -> (Response, HTTPStatus):
    if status.code == StatusCode.OK:
        return Response(status=ok_status)

    return (
        jsonify(
            ErrorResponse().dump({"description": status.description}),
        ),
        status.code.value,
    )


def model_with_list_to_response(resp: Any, schema_type: type[Schema], list_field_name="data") -> (Response, HTTPStatus):
    if len(getattr(resp, list_field_name)) == 0:
        return Response(), HTTPStatus.NOT_FOUND

    return (
        jsonify(
            schema_type().dump(resp),
        ),
        HTTPStatus.OK,
    )


def to_response(
    resp: Any, schema_type: type[Schema] | None = None, ok_status_code: HTTPStatus = HTTPStatus.OK
) -> (Response, HTTPStatus):
    if isinstance(resp, Status):
        return status_to_response(resp)

    if isinstance(resp, UserListResponse):
        return model_with_list_to_response(resp, UserInfoListSchema, "users")

    if isinstance(resp, PolicyListResponse):
        return model_with_list_to_response(resp, PolicyListSchema, "policies")

    if isinstance(resp, LogInHistoryResponse):
        return model_with_list_to_response(resp, LogInHistoryResponseSchema)

    if schema_type:
        return (
            jsonify(
                schema_type().dump(resp),
            ),
            ok_status_code,
        )

    return Response(), HTTPStatus.INTERNAL_SERVER_ERROR
