from flask import Blueprint

from api.v1.admin.policy import PolicyView, PolicyListView
from api.v1.admin.user import UserView, UserListView
from core.rate_limit import get_rate_limiter
from core.settings import get_settings

admin_blueprint = Blueprint("role_blueprint", __name__, url_prefix="/admin")

if limit := get_settings().rate_limit.blueprint.admin:
    get_rate_limiter().limit(limit)(admin_blueprint)

admin_blueprint.add_url_rule("/policies/<id>", view_func=PolicyView.as_view("policy"))
admin_blueprint.add_url_rule("/policies", view_func=PolicyListView.as_view("policy_list"))

admin_blueprint.add_url_rule("/users/<id>", view_func=UserView.as_view("user"), methods=["GET"])
admin_blueprint.add_url_rule("/users", view_func=UserListView.as_view("users"), methods=["GET"])
