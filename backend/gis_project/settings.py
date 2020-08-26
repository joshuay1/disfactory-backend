"""
Django settings for gis_project project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import pathlib
import warnings


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get("DISFACTORY_BACKEND_SECRET_KEY","!6m1_y3-d#07typf2v^te0z+1pz!i0+y!2n-c5)1by3ux2=*(q")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DISFACTORY_BACKEND_DEBUG", "true").lower() == "true"

# get allowed_host from env, if in DEBUG mode, add local hosts in

allowed_hosts = []

hosts_in_env = os.environ.get("DISFACTORY_ALLOWED_HOST", None)
print(hosts_in_env)

if hosts_in_env != None:
    try:
        for host in hosts_in_env.split(","):
            allowed_hosts.append(host.split(";")[0])
    except:
        print("error occurs when parsing allowed_hosts, please check the environment variable `DISFACTORY_ALLOWED_HOST`")
else:
    print("can't read allowed_hosts, please check the environment variable `DISFACTORY_ALLOWED_HOST`")

ALLOWED_HOSTS = allowed_hosts

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # for gis
    "django.contrib.gis",
    # 3rd party
    "rest_framework",
    "corsheaders",
    "django_q",
    "django_db_logger",
    "rangefilter",
    "mapwidgets",

    # Local
    "users.apps.UsersConfig",
    "api.apps.ApiConfig",
]

if DEBUG:
    DJANGO_LOGGER_HANDLER = ["file", "console", "db"]
else:
    DJANGO_LOGGER_HANDLER = ["db", "file", "console"]  # no need to log to console and file since we cannot access both on middle2
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "format": "%(asctime)s [%(levelname)s] %(message)s (%(module)s %(lineno)d)"
            }
        },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.environ.get("DISFACTORY_BACKEND_LOG_FILE", "./debug.log"),
            "formatter": "basic"
        },
        "console": {
            "class": "logging.StreamHandler",
        },
        "db": {
            'class': 'django_db_logger.db_log_handler.DatabaseLogHandler'
        },
    },
    "loggers": {
        "django": {
            "handlers": DJANGO_LOGGER_HANDLER,
            "level": os.environ.get("DISFACTORY_BACKEND_LOG_LEVEL", "INFO"),
            "propagate": True,
        },
    },
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gis_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "gis_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.environ.get("DISFACTORY_BACKEND_DEFAULT_DB_NAME", "postgres"),
        "USER": os.environ.get("DISFACTORY_BACKEND_DEFAULT_DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DISFACTORY_BACKEND_DEFAULT_DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DISFACTORY_BACKEND_DEFAULT_DB_HOST", "db"),
        "PORT": os.environ.get("DISFACTORY_BACKEND_DEFAULT_DB_PORT", 5432),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = "./static/"
STATIC_URL = "/static/"
AUTH_USER_MODEL = "users.CustomUser"

POSTGIS_SRID = 3857
# ref: https://epsg.io/3857

IMGUR_CLIENT_ID = os.environ.get("DISFACTORY_IMGUR_CLIENT_ID")
if IMGUR_CLIENT_ID is None:
    warnings.warn(
        "Imgur Client ID is not provided, some image related API may not work. "
        "To enable it, provide DISFACTORY_IMGUR_CLIENT_ID as a environment variable."
    )

DEFAULT_CORS_ORIGIN_WHITELIST = [
    "https://dev.disfactory.tw",
    "https://disfactory.tw",
]
CORS_ORIGIN_WHITELIST = os.environ.get('DISFACTORY_BACKEND_CORS_ORIGIN_WHITELIST')
if CORS_ORIGIN_WHITELIST is None or CORS_ORIGIN_WHITELIST == '':
    CORS_ORIGIN_WHITELIST = DEFAULT_CORS_ORIGIN_WHITELIST
else:
    CORS_ORIGIN_WHITELIST = DEFAULT_CORS_ORIGIN_WHITELIST + CORS_ORIGIN_WHITELIST.split(',')

TAIWAN_MAX_LATITUDE = 25.298401
TAIWAN_MIN_LATITUDE = 21.896900
TAIWAN_MAX_LONGITUDE = 122.007164
TAIWAN_MIN_LONGITUDE = 120.035141

MAX_FACTORY_PER_GET = int(os.environ.get("DISFACTORY_BACKEND_MAX_FACTORY_PER_GET", 50))

Q_CLUSTER = {
    'name': 'disfactory',
    'workers': 4,
    'recycle': 50,
    'timeout': 60,
    'compress': True,
    'cpu_affinity': 1,
    'label': 'Django Q',
    'orm': 'default',
    'bulk': 4,
}

# Map Widgets
MAP_WIDGETS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("mapCenterLocationName", "taipei"),
        ("GooglePlaceAutocompleteOptions", {'componentRestrictions': {'country': 'tw'}}),
        ("markerFitZoom", 12),
    ),
    "GOOGLE_MAP_API_KEY": "AIzaSyC3mo0SxFn5H8hWRq19Nk0ZBRkWT6XQDYs"
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get('DISFACTORY_BACKEND_MEDIA_ROOT', '/tmp')
pathlib.Path(MEDIA_ROOT).mkdir(parents=True, exist_ok=True)
DOMAIN = os.environ.get('DISFACTORY_BACKEND_DOMAIN', 'https://api.disfactory.tw/')
