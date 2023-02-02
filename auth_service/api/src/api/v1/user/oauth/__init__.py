from flask import Blueprint

from api.v1.user.oauth.google import oauth_google_account_blueprint
from api.v1.user.oauth.yandex import oauth_yandex_account_blueprint

oauth_account_blueprint = Blueprint("oauth_account_blueprint", __name__, url_prefix="/oauth")

oauth_account_blueprint.register_blueprint(oauth_google_account_blueprint)
oauth_account_blueprint.register_blueprint(oauth_yandex_account_blueprint)
