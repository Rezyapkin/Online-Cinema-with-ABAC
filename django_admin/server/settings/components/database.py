import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("ADMIN_PANEL_POSTGRES_DB"),
        "USER": os.environ.get("ADMIN_PANEL_POSTGRES_USER"),
        "PASSWORD": os.environ.get("ADMIN_PANEL_POSTGRES_PASSWORD"),
        "HOST": os.environ.get("ADMIN_PANEL_POSTGRES_HOST"),
        "PORT": os.environ.get("ADMIN_PANEL_POSTGRES_PORT"),
        "OPTIONS": {"options": "-c search_path=public,content"},
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
