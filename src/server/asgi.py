
import os

from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings.production_settings')   # for vercel deployment

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings.local_settings')



application = get_asgi_application()

app = application # for vercel deployment