from enum import Enum
from http import HTTPStatus
from typing import Callable, Any, TypeVar
from functools import wraps
from ipaddress import ip_address

import flask
from flask import request
from marshmallow import ValidationError, Schema, INCLUDE, EXCLUDE

from api.v1.schemas.connect_info import ConnectionInfo
from api.v1.schemas.error_response import ErrorResponse
from core.settings import get_settings


def extract_jwt(fn: Callable) -> Any:
    @wraps(fn)
    def wrapper(*args, **kwargs) -> Any:

        if token := request.headers.get("Authorization"):
            description = token.split(" ")
            if description[0] == "Bearer" and len(description) > 1:
                return fn(*args, token=description[1], **kwargs)

        return (
            flask.jsonify(
                ErrorResponse().dump({"description": "Authorization Bearer token missed"}),
            ),
            HTTPStatus.UNAUTHORIZED,
        )

    return wrapper


SchemaType = TypeVar("SchemaType", bound=Schema)


class ParametersPosition(Enum):
    BODY = 0
    QUERY = 1
    PATH = 2


def extract_parameters(
    fn: Callable | None = None,
    *,
    schema_type: type[SchemaType],
    many_schemas: bool = False,
    pos: ParametersPosition = ParametersPosition.BODY,
    extra_params: bool = False,
) -> Any:
    def decorator_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            parameters = schema_type(many=many_schemas)

            if pos == pos.BODY:
                target = request.json
            elif pos == pos.QUERY:
                target = request.args
            else:
                target = request.view_args

            try:
                data = parameters.load(target, unknown=(INCLUDE if extra_params else EXCLUDE))
            except ValidationError as e:
                return (
                    flask.jsonify(
                        ErrorResponse().dump(
                            {"description": "Wrong format: {}".format(",".join(e.messages_dict.keys()))}
                        ),
                    ),
                    HTTPStatus.UNPROCESSABLE_ENTITY,
                )

            return func(*args, parameters=data, **kwargs)

        return wrapper

    if fn is None:
        return decorator_wrapper

    return decorator_wrapper(fn)


def extract_connect_info(fn: Callable) -> Any:
    @wraps(fn)
    def wrapper(*args, **kwargs) -> Any:
        info = ConnectionInfo(
            user_ip=ip_address(request.remote_addr),
            user_agent=request.user_agent.string,
        )
        return fn(*args, connect_info=info, **kwargs)

    return wrapper


def get_full_url(endpoint: str):
    return f"{get_settings().host}{endpoint}"
