from flask import Blueprint

from core.rate_limit import get_rate_limiter
from core.settings import get_settings
from api.v1.auth.oauth.google.redirect_to_oauth import GoogleOAuthUrlRedirectView
from api.v1.auth.oauth.google.login import GoogleOAuthLogInView

oauth_google_blueprint = Blueprint("oauth_google_blueprint", __name__, url_prefix="/google")

if limit := get_settings().rate_limit.blueprint.admin:
    get_rate_limiter().limit(limit)(oauth_google_blueprint)
oauth_google_blueprint.add_url_rule(
    "/redirect_to_auth", view_func=GoogleOAuthUrlRedirectView.as_view("google_oauth_url_redirect")
)
oauth_google_blueprint.add_url_rule("/login", view_func=GoogleOAuthLogInView.as_view("google_oauth_login"))
