import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.production_settings')

application = get_wsgi_application()
