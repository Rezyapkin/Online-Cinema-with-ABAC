# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
from pathlib import Path

from server.settings.components import BASE_DIR

STATIC_URL = "/static/"
STATIC_ROOT = Path(BASE_DIR).joinpath("static")

MEDIA_ROOT = Path(BASE_DIR).joinpath("media")
MEDIA_URL = "/media/"
