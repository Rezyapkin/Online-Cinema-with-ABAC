from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from core.settings import get_settings


_rate_limiter: Limiter | None = Limiter(
    get_remote_address,
    enabled=not get_settings().testing,
    default_limits=get_settings().rate_limit.default.split(","),
    storage_uri=str(get_settings().rate_limit_redis_dsn),
    storage_options={"socket_connect_timeout": 30},
    strategy="moving-window",
)


def get_rate_limiter() -> Limiter:
    return _rate_limiter
