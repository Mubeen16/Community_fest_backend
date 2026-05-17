import os

import dj_database_url

from config.settings.base import *

DEBUG = False

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

_security_index = MIDDLEWARE.index("django.middleware.security.SecurityMiddleware")
MIDDLEWARE.insert(_security_index + 1, "whitenoise.middleware.WhiteNoiseMiddleware")

DATABASES = {
    "default": dj_database_url.config(conn_max_age=600),
}

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]
