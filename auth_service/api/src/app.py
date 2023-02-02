import grpc
from flask import Flask
from pydantic import AnyUrl

from api import blueprint
from core.logger import configure_logger
from core.rate_limit import get_rate_limiter
from core.tracer import setup_tracer
from services.utils import grpc_utils
from core.settings import get_settings
from core.open_api import create_swagger


def create_grpc_channel(dsn: AnyUrl):
    grpc_utils.grpc_channel = grpc.insecure_channel(
        dsn,
        options=[
            ("grpc.lb_policy_name", "round_robin"),
            ("grpc.enable_retries", 0),
            ("grpc.keepalive_timeout_ms", 1000),
        ],
    )


def create_app() -> Flask:
    settings = get_settings()
    application = Flask(__name__)
    configure_logger(application, settings.log_level, settings.log_folder)
    get_rate_limiter().init_app(application)
    create_swagger(application)
    application.register_blueprint(blueprint)
    if not settings.testing:
        setup_tracer(app=application)
    create_grpc_channel(settings.grpc_dsn)
    return application


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
