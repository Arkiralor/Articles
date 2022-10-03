from pathlib import Path
from os import environ, path, makedirs
from datetime import timedelta

from core.apps import DEFAULT_APPS, THIRD_PARTY_APPS, CUSTOM_APPS
from core.middleware import DEFAULT_MIDDLEWARE, THIRD_PARTY_MIDDLEWARE, CUSTOM_MIDDLEWARE

ENV_TYPE = environ.get('ENV_TYPE', 'prod').lower()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = environ['SECRET_KEY']

DEBUG = eval(environ['DEBUG'])


ALLOWED_HOSTS = environ['ALLOWED_HOSTS'].split(', ')


INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + CUSTOM_APPS
MIDDLEWARE = DEFAULT_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE + CUSTOM_MIDDLEWARE

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ['PGDATABASE'],
        'HOST': environ['PGHOST'],
        'PORT': environ['PGPORT'],
        'USER': environ['PGUSER'],
        'PASSWORD': environ['PGPASSWORD'],
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    ## prithoo: We WANT this to break if it cannot find the algorithm.
    'ALGORITHM': environ['JWT_ALGORITHM'],
    'SIGNING_KEY': SECRET_KEY,
}
if ENV_TYPE == "dev":
    SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(hours=8)
    SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"] = timedelta(days=30)

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

REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    # )
}


## Create directory for logs
LOG_DIR = path.join(BASE_DIR.parent, 'BackendLogs/')
if not path.exists(LOG_DIR):
    makedirs(LOG_DIR)
ENV_LOG_FILE = path.join(LOG_DIR, f'{ENV_TYPE}_root.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s|%(asctime)s.%(msecs)d|%(name)s|%(module)s|%(funcName)s:%(lineno)s]    %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
        'local': {
            'format': '[%(asctime)s|%(name)s|%(module)s|%(funcName)s:%(lineno)s]    %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'root_file': {
            'class': 'logging.FileHandler',
            'filename': ENV_LOG_FILE,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        }
    },
    'loggers': {
        'root': {
            'handlers': ['console', 'root_file'],
            "level": 'INFO'
        }
    },
}


LANGUAGE_CODE = environ['LANGUAGE_CODE']
TIME_ZONE = environ['TIME_ZONE']
USE_I18N = eval(environ['USE_I18N'])
USE_TZ = eval(environ['USE_TZ'])

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    path.join(BASE_DIR, 'static/')
]
MEDIA_URL = '/media/'
MEDIA_ROOT = path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'user_app.UserAccount'
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_WHITELIST = environ.get('CORS_ORIGIN_WHITELIST', '').split(', ')


OTP_ATTEMPT_LIMIT = int(environ.get('OTP_ATTEMPT_LIMIT', 10000))
OTP_ATTEMPT_TIMEOUT = int(environ.get('OTP_ATTEMPT_TIMEOUT', 0))
OTP_EXPIRY_MINUTES = int(environ.get("OTP_EXPIRY_MINUTES", 10))

ITEMS_PER_PAGE = 10


