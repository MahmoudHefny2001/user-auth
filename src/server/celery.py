import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings.base_settings")

app = Celery("server")

from server import celery

# Adjust the import statement to correctly import the settings
app.config_from_object("server.settings.base_settings", namespace="CELERY")

app.autodiscover_tasks()
