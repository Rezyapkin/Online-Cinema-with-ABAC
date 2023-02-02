from flask import Blueprint

from api.v1 import v1_blueprint

blueprint = Blueprint("api_blueprint", __name__, url_prefix="/api")

blueprint.register_blueprint(v1_blueprint)
