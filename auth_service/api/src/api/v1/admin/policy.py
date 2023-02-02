from http import HTTPStatus
from flasgger import SwaggerView
from flask import Response

from api.v1.convert_to_response import to_response
from api.v1.schemas.error_response import ErrorResponse
from api.utils import (
    extract_jwt,
    extract_connect_info,
    extract_parameters,
    ParametersPosition,
)
from api.v1.schemas.connect_info import ConnectionInfo
from api.v1.schemas.admin.id import IdSchema
from api.v1.schemas.admin.policy import (
    Policy,
    PolicySchema,
    PolicyListSchema,
    PolicyRequestSchema,
    PolicyListRequestSchema,
    PolicyListRequest,
)
from services.admin import get_admin_service


class PolicyView(SwaggerView):
    decorators = [
        extract_jwt,
        extract_connect_info,
    ]
    summary = "Policy"
    definitions = {
        "PolicySchema": PolicySchema,
    }
    tags = ["admin"]
    security = [{"bearerAuth": []}]
    consumes = ["application/json"]
    produces = ["application/json"]
    responses = {
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
            "description": "Policy not found",
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
        Get policy by `id`
        ---
        parameters:
            - in: path
              name: id
              schema:
                type: string
                example: b14405b2-92ee-4360-975f-a9c8e397278a
        responses:
            '200':
              description: Get policy by `id`
              content:
                application/json:
                  schema:
                    $ref: '#/definitions/PolicySchema'
                  example: |-
                    {
                        "policy": {
                            "id": "b14405b2-92ee-4360-975f-a9c8e397278a",
                            "effect": "allow",
                            "subjects": [
                                {
                                    "name": {
                                        "rule_type": "RuleAny"
                                    },
                                    "stars": {
                                        "rule_type": "And",
                                        "rules": [
                                            {
                                                "rule_type": "Greater",
                                                "value": 50
                                            },
                                            {
                                                "rule_type": "Less",
                                                "value": 999
                                            }
                                        ]
                                    }
                                }
                            ],
                            "resources": [
                                {
                                    "repo": {
                                        "rule_type": "StrStartsWith",
                                        "value": "repos/Google",
                                        "case_sensitive": true
                                    }
                                }
                            ],
                            "actions": [
                                {
                                    "rule_type": "Eq",
                                    "value": "fork"
                                },
                                {
                                    "rule_type": "Eq",
                                    "value": "clone"
                                }
                            ],
                            "context": {
                                "referer": {
                                    "rule_type": "Eq",
                                    "value": "https://github.com"
                                }
                            },
                            "description": "Allow to fork or clone any Google repository for users that have > 50..."
                        }
                    }
        """
        answer = get_admin_service().get_policy(PolicyRequestSchema().load({"id": id}).to_model(connect_info, token))
        return to_response(answer, PolicySchema)

    def delete(self, token: str, connect_info: ConnectionInfo, id: str) -> Response:
        """
        Delete policy by `id`
        ---
        parameters:
            - in: path
              name: id
              schema:
                type: string
                example: b14405b2-92ee-4360-975f-a9c8e397278a
        responses:
            '204':
              description: Policy was successfully deleted
        """
        answer = get_admin_service().delete_policy(PolicyRequestSchema().load({"id": id}).to_model(connect_info, token))
        return to_response(answer)

    @extract_parameters(schema_type=PolicySchema)
    def put(self, token: str, connect_info: ConnectionInfo, id: str, parameters: Policy) -> Response:
        """
        Update policy
        ---
        parameters:
            - in: path
              name: id
              schema:
                type: string
                example: b14405b2-92ee-4360-975f-a9c8e397278a
        requestBody:
           content:
               application/json:
                   schema:
                       $ref: '#/definitions/PolicySchema'
                   example: |-
                    {
                        "policy": {
                            "effect": "allow",
                            "subjects": [
                                {
                                    "name": {
                                        "rule_type": "RuleAny"
                                    },
                                    "stars": {
                                        "rule_type": "And",
                                        "rules": [
                                            {
                                                "rule_type": "Greater",
                                                "value": 50
                                            },
                                            {
                                                "rule_type": "Less",
                                                "value": 999
                                            }
                                        ]
                                    }
                                }
                            ],
                            "resources": [
                                {
                                    "repo": {
                                        "rule_type": "StrStartsWith",
                                        "value": "repos/Google",
                                        "case_sensitive": true
                                    }
                                }
                            ],
                            "actions": [
                                {
                                    "rule_type": "Eq",
                                    "value": "fork"
                                },
                                {
                                    "rule_type": "Eq",
                                    "value": "clone"
                                }
                            ],
                            "context": {
                                "referer": {
                                    "rule_type": "Eq",
                                    "value": "https://github.com"
                                }
                            },
                            "description": "Allow to fork or clone any Google repository for users that have > 50..."
                        }
                    }
                   required: true
        responses:
            '204':
              description: Policy was successfully updated
        """

        answer = get_admin_service().update_policy(parameters.to_update_model(id, connect_info, token))
        return to_response(answer)


class PolicyListView(SwaggerView):
    decorators = [
        extract_jwt,
        extract_connect_info,
    ]
    summary = "Policy"
    definitions = {
        "PolicySchema": PolicySchema,
        "PolicyListSchema": PolicyListSchema,
        "PolicyListRequestSchema": PolicyListRequestSchema,
        "IdSchema": IdSchema,
    }
    tags = ["admin"]
    security = [{"bearerAuth": []}]
    consumes = ["application/json"]
    produces = ["application/json"]
    responses = {
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

    @extract_parameters(schema_type=PolicyListRequestSchema, pos=ParametersPosition.QUERY)
    def get(self, token: str, connect_info: ConnectionInfo, parameters: PolicyListRequest) -> Response:
        """
        Get list of policies
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
        responses:
            '200':
              description: List of policies
              content:
                application/json:
                  schema:
                    $ref: '#/definitions/PolicyListSchema'
                  example: |-
                    {
                        "policies": [{
                            "id": "b14405b2-92ee-4360-975f-a9c8e397278a",
                            "effect": "allow",
                            "subjects": [
                                {
                                    "name": {
                                        "rule_type": "RuleAny"
                                    },
                                    "stars": {
                                        "rule_type": "And",
                                        "rules": [
                                            {
                                                "rule_type": "Greater",
                                                "value": 50
                                            },
                                            {
                                                "rule_type": "Less",
                                                "value": 999
                                            }
                                        ]
                                    }
                                }
                            ],
                            "resources": [
                                {
                                    "repo": {
                                        "rule_type": "StrStartsWith",
                                        "value": "repos/Google",
                                        "case_sensitive": true
                                    }
                                }
                            ],
                            "actions": [
                                {
                                    "rule_type": "Eq",
                                    "value": "fork"
                                },
                                {
                                    "rule_type": "Eq",
                                    "value": "clone"
                                }
                            ],
                            "context": {
                                "referer": {
                                    "rule_type": "Eq",
                                    "value": "https://github.com"
                                }
                            },
                            "description": "Allow to fork or clone any Google repository for users that have > 50..."
                        }, ],
                        "pagination": {
                            "total_count": 20,
                            "total_pages": 2,
                            "next_page": 2
                        }
                    }
        """

        answer = get_admin_service().get_policy_list(parameters.to_model(connect_info, token))
        return to_response(answer)

    @extract_parameters(schema_type=PolicySchema)
    def post(self, token: str, connect_info: ConnectionInfo, parameters: Policy) -> Response:
        """
        Create new policy
        ---
        requestBody:
           content:
               application/json:
                   schema:
                       $ref: '#/definitions/PolicySchema'
                   example: |-
                    {
                        "policy": {
                            "effect": "allow",
                            "subjects": [
                                {
                                    "name": {
                                        "rule_type": "RuleAny"
                                    },
                                    "stars": {
                                        "rule_type": "And",
                                        "rules": [
                                            {
                                                "rule_type": "Greater",
                                                "value": 50
                                            },
                                            {
                                                "rule_type": "Less",
                                                "value": 999
                                            }
                                        ]
                                    }
                                }
                            ],
                            "resources": [
                                {
                                    "repo": {
                                        "rule_type": "StrStartsWith",
                                        "value": "repos/Google",
                                        "case_sensitive": true
                                    }
                                }
                            ],
                            "actions": [
                                {
                                    "rule_type": "Eq",
                                    "value": "fork"
                                },
                                {
                                    "rule_type": "Eq",
                                    "value": "clone"
                                }
                            ],
                            "context": {
                                "referer": {
                                    "rule_type": "Eq",
                                    "value": "https://github.com"
                                }
                            },
                            "description": "Allow to fork or clone any Google repository for users that have > 50 ..."
                        }
                    }
                   required: true
        responses:
            "201":
              description: Policy was successfully created
              content:
                application/json:
                  schema:
                    $ref: "#/definitions/IdSchema"
                  example: |-
                    {
                        "id": "b14405b2-92ee-4360-975f-a9c8e397278a",
                    }
        """
        answer = get_admin_service().create_policy(parameters.to_create_model(connect_info, token))
        return to_response(answer, IdSchema, HTTPStatus.CREATED)
