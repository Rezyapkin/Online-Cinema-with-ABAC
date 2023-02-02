from flask import Blueprint

from api.v1.auth.oauth import oauth_blueprint
from api.v1.auth.login import LogInPostView
from api.v1.auth.logout import LogOutPostView
from api.v1.auth.refresh import RefreshPostView
from api.v1.auth.change_email import NewEmailPostView
from api.v1.auth.change_password import NewPasswordPostView
from core.rate_limit import get_rate_limiter
from core.settings import get_settings

auth_blueprint = Blueprint("auth_blueprint", __name__, url_prefix="/auth")

if limit := get_settings().rate_limit.blueprint.auth:
    get_rate_limiter().limit(limit)(auth_blueprint)

auth_blueprint.register_blueprint(oauth_blueprint)

auth_blueprint.add_url_rule("/login/email", view_func=LogInPostView.as_view("login_email"), methods=["POST"])

auth_blueprint.add_url_rule("/logout", view_func=LogOutPostView.as_view("logout"), methods=["POST"])

auth_blueprint.add_url_rule("/refresh", view_func=RefreshPostView.as_view("refresh"), methods=["POST"])

auth_blueprint.add_url_rule("/change_password", view_func=NewPasswordPostView.as_view("password"), methods=["POST"])

auth_blueprint.add_url_rule("/change_email", view_func=NewEmailPostView.as_view("email"), methods=["POST"])
