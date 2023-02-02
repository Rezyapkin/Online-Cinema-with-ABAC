from http import HTTPStatus

from flasgger import SwaggerView
from flask import Response, redirect, url_for

from services.oauth.yandex import get_oauth_yandex_service
from api.v1.convert_to_response import status_to_response
from api.v1.schemas.error_response import ErrorResponse
from api.v1.schemas.connect_info import ConnectionInfo
from api.v1.schemas.oauth.get_login_url import GetLoginUrlRequest
from api.utils import extract_connect_info, get_full_url
from models.status import Status


REDIRECT_ENDPOINT = ".yandex_oauth_login"


class YandexOAuthUrlRedirectView(SwaggerView):
    decorators = [
        extract_connect_info,
    ]
    summary = "OAuth"
    description = "Redirect to the Yandex OAuth 2.0 authentication page"
    tags = ["oauth"]
    consumes = ["application/json"]
    produces = ["application/json"]
    responses = {
        HTTPStatus.FOUND.value: {
            "description": "Redirect to the Yandex OAuth 2.0 authentication page",
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

    def get(self, connect_info: ConnectionInfo) -> Response:
        """
        Redirect to Yandex OAuth 2.0 for authentication.
        ---
        """
        callback_url = get_full_url(url_for(REDIRECT_ENDPOINT))
        answer = get_oauth_yandex_service().get_provider_login_url(
            GetLoginUrlRequest(callback_url=callback_url).to_model(connect_info)
        )

        if isinstance(answer, Status):
            return status_to_response(answer)

        return redirect(answer.url)
