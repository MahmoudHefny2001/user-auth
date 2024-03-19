import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.production_settings')   # for vercel deployment

application = get_wsgi_application()

app = application  # for vercel deployment
