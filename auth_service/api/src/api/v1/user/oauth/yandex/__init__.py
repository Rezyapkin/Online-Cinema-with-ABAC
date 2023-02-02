from flask import Blueprint

from core.rate_limit import get_rate_limiter
from core.settings import get_settings
from api.v1.user.oauth.yandex.redirect_to_attach import YandexOAuthAttachUrlRedirectView
from api.v1.user.oauth.yandex.attach import AttachYandexAccountView
from api.v1.user.oauth.yandex.detach import DetachYandexAccountView

oauth_yandex_account_blueprint = Blueprint("oauth_yandex_account_blueprint", __name__, url_prefix="/yandex")

if limit := get_settings().rate_limit.blueprint.admin:
    get_rate_limiter().limit(limit)(oauth_yandex_account_blueprint)

oauth_yandex_account_blueprint.add_url_rule(
    "/redirect_to_attach", view_func=YandexOAuthAttachUrlRedirectView.as_view("yandex_oauth_attach_url_redirect")
)
oauth_yandex_account_blueprint.add_url_rule(
    "/attach", view_func=AttachYandexAccountView.as_view("yandex_oauth_account_attach")
)
oauth_yandex_account_blueprint.add_url_rule(
    "", view_func=DetachYandexAccountView.as_view("yandex_oauth_account_detach"), methods=["DELETE"]
)
