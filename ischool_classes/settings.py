"""
Django settings for ischool_classes project. This project is based on the 
iSchool at Syracuse University's base starter project

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Ischool API Auth
ISCHOOL_API_HOST = "https://api.ischool.syr.edu/api/"
ISCHOOL_API_USER = "apiuser"
ISCHOOL_API_PASSWORD = "testing123"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_ENV=os.environ.get("APP_ENV", "testing")
APP_ENV_LOCAL=os.environ.get("APP_ENV_LOCAL", "true")
APP_HOST=os.environ.get("APP_HOST", "localhost")
DATABASE_DB=os.environ.get("DATABASE_DB", "testdb")
DATABASE_HOST=os.environ.get("DATABASE_HOST", "10.0.75.1")
DATABASE_USER=os.environ.get("DATABASE_USER", "ischooldevdbuser")
DATABASE_PASSWORD=os.environ.get("DATABASE_PASSWORD", "ischooldev")
DATABASE_ENGINE=os.environ.get("DATABASE_ENGINE", "django.db.backends.sqlite3")
DATABASE_PORT=os.environ.get("DATABASE_PORT", "5432")
RABBIT_HOST = os.environ.get("RABBIT_HOST", "")
RABBIT_USER  = os.environ.get("RABBIT_USER", "")
RABBIT_PASSWORD = os.environ.get("RABBIT_PASSWORD", "")
CACHE_SERVER = os.environ.get("CACHE_SERVER", "")

IDENTITY_SERVER_URL = os.environ.get("IDENTITY_SERVER_URL", "https://sso4.ischool.syr.edu/")
IDENTITY_SERVER_APIID = os.environ.get("IDENTITY_SERVER_APIID", "edu.syr.ischool.ischool_classes")
IDENTITY_SERVER_API_SECRET = os.environ.get("IDENTITY_SERVER_API_SECRET", "")

PROXY_SERVERS = {}



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#tcj*b5#$-s(d4i@npcqp_x-i9xjw01kk5zdrnm%x39*t)7x1i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if APP_ENV == "development" or APP_ENV == "testing":
    DEBUG = True


ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Nick', 'ndlyga@syr.edu'),
    ('Mike', 'mmclarke@syr.edu'),
)


# Application definition


INSTALLED_APPS = [
    #'django.contrib.contenttypes',
    'django.contrib.postgres',
    'django.contrib.staticfiles',
    'drf_yasg',
    'storages',
    'ischool_storage',
    'rest_framework',
    'corsheaders',
    'ischool_classes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ischool_classes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True if APP_ENV == "testing" else False,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                #'django.contrib.auth.context_processors.auth',
                "django.template.context_processors.tz",
            ],
        },
    },
]

WSGI_APPLICATION = 'ischool_classes.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# if APP_ENV == "testing":
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': 'testdatabase',
#         }
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': DATABASE_ENGINE,
#             'NAME': DATABASE_DB,
#             'HOST': DATABASE_HOST,
#             'USER': DATABASE_USER,
#             'PASSWORD': DATABASE_PASSWORD,
#             'PORT': DATABASE_PORT
#         }
#     }

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'testdatabase',
        }
    }

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        "ischool_auth": {
            "type": "oauth2",
            "authorizationUrl": "https://sso4.ischool.syr.edu/connect/authorize",
            "flow": "implicit",
            "scopes": {
                "read:classes": "view classes",
                "write:waitlist": "add to waitlist",
            }
        }
    },
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        #'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
       'rest_framework.parsers.JSONParser',
    ),
    'UNAUTHENTICATED_USER': 'auth_core.auth_backends.user_models.AnonymousUser',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 200,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'auth_core.auth_backends.api_identity_auth.AccessTokenIdentityServerAuth',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
}

# https://github.com/ottoyiu/django-cors-headers/
if APP_ENV == "testing":
    CORS_ORIGIN_ALLOW_ALL = True
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = ('auth_core.auth_backends.dev_auth_backend.DevelopAPIAuthentication', )
elif APP_ENV == "development":
    CORS_ORIGIN_WHITELIST = (
        '127.0.0.1:4200',
        'localhost:4200',
        'staging.my-ischool.dev.ischool.syr.edu',
    )
else:
    CORS_ORIGIN_REGEX_WHITELIST = (r'^(https?://)?(\w+\.)?ischool\.syr\.com$', r'^(https?://)?(\w+\.)?ischool\.syr\.local$', r'^(https?://)?(\w+\.)?ischool\.syr\.local$')


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


if APP_ENV == "testing":
    STATIC_URL = '/static/'
    STATIC_ROOT = os.environ.get("STATIC_ROOT", '/ischool_classes/')
else:
    STATIC_URL = os.environ.get("STATIC_URL", 'https://storage2.ischool.syr.edu/api.ischool.syr.edu/ischool_classes/')
    STATIC_ROOT = os.environ.get("STATIC_ROOT", '/ischool_classes/')
    STATICFILES_STORAGE = 'ischool_storage.storage.StaticS3Boto3Storage'


MEDIA_ROOT = STATIC_ROOT + "media/"
MEDIA_URL = "/".join((STATIC_URL.rstrip("/"), "media", ""))

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "a2PYqPqhQJWSKnmuTL6l")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "6cHc!376JYn#[:P!")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "api.ischool.syr.edu")
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL", "https://storage2.ischool.syr.edu")

# Django Storages
DEFAULT_FILE_STORAGE = 'ischool_storage.storage.MediaS3Storage'

AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_QUERYSTRING_AUTH = False
AWS_IS_GZIPPED = True

GZIP_CONTENT_TYPES = (
    'text/css',
    'application/javascript',
    'application/x-javascript',
    'text/javascript'
)

