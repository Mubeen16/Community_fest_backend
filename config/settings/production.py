import os

import dj_database_url

from config.settings.base import *

DEBUG = False

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
    )
}

CORS_ALLOWED_ORIGINS = [
    "https://london-community-fest.vercel.app",
]

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
