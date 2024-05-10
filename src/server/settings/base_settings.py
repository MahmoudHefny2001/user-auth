from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

import os

from datetime import timedelta

from dotenv import load_dotenv

load_dotenv("environments/.env.production")


SECRET_KEY = os.environ.get("SECRET_KEY",)

DEBUG = False

ALLOWED_HOSTS = list(str(os.environ.get("ALLOWED_HOSTS")).split(", "))


HOST_URL = os.environ.get("HOST_URL")


# Application definition

INSTALLED_APPS = [
    'jazzmin', # 
    'corsheaders',  #
    'rest_framework_swagger', #
    'drf_yasg', #

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "rest_framework", #
    'rest_framework_simplejwt', #
    'django_extensions',
    'django_filters', #
    "models_extensions", #

    # apps

    "apps.users", #
    "apps.products", #
    "apps.customers", #
    "apps.orders", #
    "apps.carts", #
    "apps.wishlists", #
    "apps.contacts", #
    "apps.admins", #
    "apps.merchants", #
    "apps.stocks", #
    "apps.reviews", #
    "apps.payments", #

    # "apps.notifications", #
    # "apps.shipments", #
    
]

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get("REDIS_URL"),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Celery settings
CELERY_BROKER_URL = os.environ.get("REDIS_BROKER_URL")
RESULT_BACKEND = os.environ.get("REDIS_RESULT_BACKEND_URL")


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "apps.users.customJWT.CustomJWTAuthenticationClass", ##
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        'rest_framework.permissions.AllowAny',
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    # "DEFAULT_RENDERER_CLASSES": [
        # "rest_framework.renderers.JSONRenderer",
    # ],
    'DEFAULT_AUTHENTICATION_BACKENDS': [
        'django.contrib.auth.backends.ModelBackend',
    ],
    
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],

    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day',
        'user': '10000/day'
    },

    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=4),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ("JWT", "Bearer"),
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}


AUTHENTICATION_BACKENDS = [
    'apps.users.authentication.CustomUserAuthenticationBackend',
]


AUTH_USER_MODEL = "users.User"

MIDDLEWARE = [

    "corsheaders.middleware.CorsMiddleware",  ##

    'whitenoise.middleware.WhiteNoiseMiddleware',  ##
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'




AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Loacl static files
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_FILES_DIRS = [BASE_DIR / "static",]



# Loacl media files
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



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






DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


JAZZMIN_SETTINGS = {
"site_title": "Digital Hub",
"site_header": "Digital Hub",
# "site_brand": "",
# "site_logo": "",
# "site_logo_classes": "img-circle",
# "welcome_sign": "Welcome ",
# "related_modal_active": False,
"copyright": "Mahmoud Hefny",
# "show_sidebar": True,
# "navigation_expanded": True,
# "show_ui_builder": True,

"usermenu_links": [
     {'name':"Support", "url":"https://www.linkedin.com/in/mahmoud-hefny-622b721a9/"},
    ],
}



SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True


EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")

EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")

# EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST = os.environ.get("EMAIL_HOST")

# EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")

# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_PORT = os.environ.get("EMAIL_PORT")

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")

SENDINBLUE_API_KEY = os.environ.get("SENDINBLUE_API_KEY")
