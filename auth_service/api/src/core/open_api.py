from functools import lru_cache

from flasgger import Swagger
from flask import Flask

_swagger: Swagger | None = None


def create_swagger(application: Flask):
    global _swagger

    if _swagger is not None:
        return

    application.config["SWAGGER"] = {
        "title": "Authentication API",
        "description": "User authentication API",
        "openapi": "3.0.3",
        "consumes": ["application/json"],
        "produces": ["application/json"],
    }

    config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "APISpecification",
                "route": "/APISpecification",
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "specs_route": "/openapi/",
        "url_prefix": "/api",
    }
    swagger_template = {
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            },
            "security": {"bearerAuth": []},
        }
    }
    _swagger = Swagger(application, config=config, template=swagger_template, merge=False)


@lru_cache
def get_swagger() -> Swagger:
    return _swagger
