from flask import Blueprint

from core.rate_limit import get_rate_limiter
from core.settings import get_settings
from api.v1.auth.oauth.yandex.redirect_to_oauth import YandexOAuthUrlRedirectView
from api.v1.auth.oauth.yandex.login import YandexOAuthLogInView

oauth_yandex_blueprint = Blueprint("oauth_yandex_blueprint", __name__, url_prefix="/yandex")

if limit := get_settings().rate_limit.blueprint.admin:
    get_rate_limiter().limit(limit)(oauth_yandex_blueprint)
oauth_yandex_blueprint.add_url_rule(
    "/redirect_to_auth", view_func=YandexOAuthUrlRedirectView.as_view("yandex_oauth_url_redirect")
)
oauth_yandex_blueprint.add_url_rule("/login", view_func=YandexOAuthLogInView.as_view("yandex_oauth_login"))
