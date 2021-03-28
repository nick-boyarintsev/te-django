from configparser import ConfigParser
from os import getenv, path
from pathlib import Path

config = ConfigParser()
config['django'] = {
    'debug': getenv('DEBUG', '0'),
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e++y(t8(wp1=-o0()qt#e4ulk-ejxg$cscg%+&bo-pzl%8q!1u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config['django'].getboolean('debug')

if getenv('ALLOWED_HOSTS'):
    ALLOWED_HOSTS = getenv('ALLOWED_HOSTS').split(" ")
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

ADMIN_ENABLED = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom apps
    'rest_api.apps.RestApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom middleware
    'backend.middleware.XCorrelationIDMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'memcached:11211',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = path.join(BASE_DIR, 'static')
STATIC_URL = '/api/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'requests': {
            '()': 'backend.logging.RequestFilter',
        },
    },
    'formatters': {
        'standard': {
            'format': '%(levelname)-8s [%(asctime)s: %(name)s] %(message)s',
        },
        'requests': {
            'format': '%(levelname)-8s [%(asctime)s: %(name)s] [%(x_correlation_id)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'requests': {
            'class': 'logging.StreamHandler',
            'filters': ['requests'],
            'formatter': 'requests',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['requests'],
            'propagate': False,
        },
    },
}
