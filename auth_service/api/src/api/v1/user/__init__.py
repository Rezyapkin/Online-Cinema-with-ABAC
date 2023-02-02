from flask import Blueprint

from api.v1.user.oauth import oauth_account_blueprint
from api.v1.user.log_in_history import LogInHistoryGetView
from api.v1.user.sign_up import SignUpPostView
from api.v1.user.user_me import UserMeView
from core.rate_limit import get_rate_limiter
from core.settings import get_settings

user_blueprint = Blueprint("account_blueprint", __name__, url_prefix="/user")

if limit := get_settings().rate_limit.blueprint.user:
    get_rate_limiter().limit(limit)(user_blueprint)

user_blueprint.register_blueprint(oauth_account_blueprint)

user_blueprint.add_url_rule("/signup/email", view_func=SignUpPostView.as_view("signup"), methods=["POST"])
user_blueprint.add_url_rule("/login/history", view_func=LogInHistoryGetView.as_view("history"), methods=["GET"])
user_blueprint.add_url_rule("/me", view_func=UserMeView.as_view("me"), methods=["GET"])
