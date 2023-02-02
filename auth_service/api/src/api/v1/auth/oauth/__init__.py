from flask import Blueprint

from api.v1.auth.oauth.google import oauth_google_blueprint
from api.v1.auth.oauth.yandex import oauth_yandex_blueprint

oauth_blueprint = Blueprint("oauth_blueprint", __name__, url_prefix="/oauth")

oauth_blueprint.register_blueprint(oauth_google_blueprint)
oauth_blueprint.register_blueprint(oauth_yandex_blueprint)
