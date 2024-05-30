import os
from celery import Celery

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings.production_settings")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings.local_settings')



app = Celery("server")


# app.config_from_object("server.settings.production_settings", namespace="CELERY")
app.config_from_object("server.settings.local_settings", namespace="CELERY")


app.conf.broker_connection_retry_on_startup = True


app.autodiscover_tasks()
