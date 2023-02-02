import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("ADMIN_PANEL_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("ADMIN_PANEL_DEBUG", False) == "True"

ALLOWED_HOSTS = os.environ.get("ADMIN_PANEL_ALLOWED_HOSTS").split(" ")

if DEBUG:
    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

    CORS_ALLOWED_ORIGINS = ("http://127.0.0.1:8080",)
    SHELL_PLUS_PRINT_SQL_TRUNCATE = None
