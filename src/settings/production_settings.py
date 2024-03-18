from .base_settings import *


from dotenv import load_dotenv


load_dotenv(".env.production")


SECRET_KEY = os.environ.get("SECRET_KEY", None)

DEBUG = True

ALLOWED_HOSTS = list(str(os.environ.get("ALLOWED_HOSTS")).split(", "))

HOST_URL = os.environ.get("HOST_URL")



# RAILWAY_VOLUME_NAME = str(os.environ.get("RAILWAY_VOLUME_NAME"))
# RAILWAY_VOLUME_MOUNT_PATH = str(os.environ.get("RAILWAY_VOLUME_MOUNT_PATH"))

# Static files (CSS, JavaScript, Images)
# STATIC_URL = 'static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')



# Media Files (uploaded from users)
# MEDIA_URL = "media/"
# MEDIA_URL = os.environ.get("BLOB_READ_WRITE_TOKEN") ## Vercel Blob Storage
MEDIA_URL = 'https://vpz2sexxpggaxlxl.public.blob.vercel-storage.com/media/' ## Vercel Blob Storage
MEDIA_ROOT = os.path.join(BASE_DIR, "media")




DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "DATABASE_URL": str(os.environ.get("DATABASE_URL")),
        "NAME": str(os.environ.get("DATABASE_NAME")),
        "USER": str(os.environ.get("DATABASE_USER")),
        "PASSWORD": str(os.environ.get("DATABASE_PASSWORD")),
        "HOST": str(os.environ.get("DATABASE_HOST")),
        "PORT": int(os.environ.get("DATABASE_PORT")),
        # 'TEST': {
        #     'NAME': '',
        # },
    }
}


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    ]
}


