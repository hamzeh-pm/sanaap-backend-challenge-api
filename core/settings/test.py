"""
With these settings, tests run faster.
"""

from .base import *  # noqa: F403
from .base import env

# GENERAL
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="Ig7ySjchvb6bg4ibMz3Bigpm2MZ0BVDHQVTqI66BlNzHkd7eRaVQc4ToWkOWtz5c",
)


# PASSWORDS
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
