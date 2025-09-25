import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

app = Celery("sanaap_backend_challenge_api")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
