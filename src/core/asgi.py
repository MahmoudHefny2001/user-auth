
import os

from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.production_settings')   # for vercel deployment

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local_settings')   # for local development


application = get_asgi_application()

# app = application # for vercel deployment