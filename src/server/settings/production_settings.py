from .base_settings import *


from dotenv import load_dotenv


load_dotenv("environments/.env.production")


SECRET_KEY = os.environ.get("SECRET_KEY", None)

DEBUG = False


ALLOWED_HOSTS = list(str(os.environ.get("ALLOWED_HOSTS")).split(", "))

HOST_URL = os.environ.get("HOST_URL")



INSTALLED_APPS += [
    # 'cloudinary_storage', # Cloudinary Storage
    # 'cloudinary',      # Cloudinary

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]


MIDDLEWARE += [
    "allauth.account.middleware.AccountMiddleware",
]


SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v7.0',
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
            
        ],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}


AUTHENTICATION_BACKENDS += [
    'allauth.account.auth_backends.AuthenticationBackend',
]



# import cloudinary
# import cloudinary.uploader
# import cloudinary.api

# CLOUDINARY_STORAGE = {
#   	'CLOUD_NAME': os.environ.get("CLOUD_NAME"),
#   	'API_KEY': os.environ.get("API_KEY"),
#   	'API_SECRET': os.environ.get("API_SECRET")
# }
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'



MEDIA_URL = '/media/'  # or any prefix you choose
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


RAILWAY_VOLUME_NAME = str(os.environ.get("RAILWAY_VOLUME_NAME"))
RAILWAY_VOLUME_MOUNT_PATH = str(os.environ.get("RAILWAY_VOLUME_MOUNT_PATH"))
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), RAILWAY_VOLUME_MOUNT_PATH)


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
# MEDIA_URL = 'https://vpz2sexxpggaxlxl.public.blob.vercel-storage.com/media/' ## Vercel Blob Storage
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")




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



CSRF_TRUSTED_ORIGINS = [
    "http://*.",
    "http://localhost:8000",
]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_ORIGINS = [
    "http://localhost:8083",
]

CORS_ALLOWED_ORIGINS = [
    'http://*',
]



CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]


CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    'api_key',          
    'Authorization',
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "ngrok-skip-browser-warning"
    'accept-encoding',
    'dnt',
    'origin',
]
