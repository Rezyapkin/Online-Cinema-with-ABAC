from flask import Blueprint

from core.rate_limit import get_rate_limiter
from core.settings import get_settings
from api.v1.user.oauth.google.redirect_to_attach import GoogleOAuthAttachUrlRedirectView
from api.v1.user.oauth.google.attach import AttachGoogleAccountView
from api.v1.user.oauth.google.detach import DetachGoogleAccountView


oauth_google_account_blueprint = Blueprint("oauth_google_account_blueprint", __name__, url_prefix="/google")

if limit := get_settings().rate_limit.blueprint.admin:
    get_rate_limiter().limit(limit)(oauth_google_account_blueprint)

oauth_google_account_blueprint.add_url_rule(
    "/redirect_to_attach", view_func=GoogleOAuthAttachUrlRedirectView.as_view("google_oauth_attach_url_redirect")
)
oauth_google_account_blueprint.add_url_rule(
    "/attach", view_func=AttachGoogleAccountView.as_view("google_auth_account_attach")
)
oauth_google_account_blueprint.add_url_rule(
    "", view_func=DetachGoogleAccountView.as_view("google_auth_account_detach"), methods=["DELETE"]
)
