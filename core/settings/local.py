from .base import *  # noqa: F403
from .base import INSTALLED_APPS
from .base import env

DEBUG = True

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="YxKNguigYhkGbSmp7tV16z0L2kbaLuEp1BwnhitIvCJawS1M4FpEBlbPlX9MUr02",
)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]  # noqa: S104


# django-extensions
INSTALLED_APPS += ["django_extensions"]
