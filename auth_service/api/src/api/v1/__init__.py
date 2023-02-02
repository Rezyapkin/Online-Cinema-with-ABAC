from flask import Blueprint

from api.v1.admin import admin_blueprint
from api.v1.auth import auth_blueprint
from api.v1.user import user_blueprint

v1_blueprint = Blueprint("v1_blueprint", __name__, url_prefix="/v1")

v1_blueprint.register_blueprint(admin_blueprint)
v1_blueprint.register_blueprint(auth_blueprint)
v1_blueprint.register_blueprint(user_blueprint)
