from os import environ
import os
from pathlib import Path
from corsheaders.defaults import default_headers
from telegram import Bot


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = environ.get("DEBUG", "1").lower() in ("true", "1")

ALLOWED_HOSTS = environ["ALLOWED_HOSTS"].split(",")

# Cors
CORS_ORIGIN_WHITELIST = environ["CORS_ORIGIN_WHITELIST"].split(",")

CSRF_TRUSTED_ORIGINS = environ["CORS_ORIGIN_WHITELIST"].split(",")

CORS_ALLOW_HEADERS = default_headers + (
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Credentials",
    "Access-Control-Allow-Origin",
)

CORS_ALLOW_CREDENTIALS = True

# https
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Application definition

LOCAL_APPS = [
    "apps.account",
    "apps.common",
    "apps.support",
    "apps.vending",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "django_celery_beat",
    "nested_admin",
    "phonenumber_field",
]

INSTALLED_APPS = (
    [
        "unfold",
        "unfold.contrib.filters",
        "unfold.contrib.forms",
        "unfold.contrib.inlines",
        "unfold.contrib.import_export",
        "unfold.contrib.guardian",
        "unfold.contrib.simple_history",
        "core.unfold_singleton",
        "core.unfold_nested",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]
    + THIRD_PARTY_APPS
    + LOCAL_APPS
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTH_USER_MODEL = "account.User"

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": environ["POSTGRES_DB"],
        "USER": environ["POSTGRES_USER"],
        "PASSWORD": environ["POSTGRES_PASSWORD"],
        "HOST": environ["POSTGRES_HOST"],
        "PORT": environ["POSTGRES_PORT"],
        "ATOMIC_REQUESTS": True,
    }
}

# RabbitMQ
RABBITMQ = {
    "PROTOCOL": "amqp",
    "HOST": environ.get("RABBITMQ_HOST"),
    "PORT": environ.get("RABBITMQ_PORT"),
    "USER": environ.get("RABBITMQ_USER"),
    "PASSWORD": environ.get("RABBITMQ_PASSWORD"),
}

# Celery
CELERY_BROKER_URL = (
    f"{RABBITMQ['PROTOCOL']}://{RABBITMQ['USER']}"
    f":{RABBITMQ['PASSWORD']}@{RABBITMQ['HOST']}:{RABBITMQ['PORT']}"
)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_ENABLE_UTC = False
CELERY_MAX_TASKS_PER_CHILD = 1
CELERY_RESULT_BACKEND = "rpc://"
CELERY_TIMEZONE = "Europe/Moscow"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

DJANGO_CELERY_BEAT_TZ_AWARE = True

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_DIRS = [
    BASE_DIR / "staticfiles",
]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Rest framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "core.authentication.uuid_authentication.UUIDAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
}

# Logging
os.makedirs("logs", exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/django.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 7,
            "encoding": "utf-8",
            "formatter": "verbose",
        },
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}

# Telegram bot
MAIN_TELEGRAM_BOT_TOKEN = environ.get("MAIN_TELEGRAM_BOT_TOKEN")
MAIN_TELEGRAM_BOT_URL = environ.get("MAIN_TELEGRAM_BOT_URL")
MAIN_TELEGRAM_BOT = Bot(MAIN_TELEGRAM_BOT_TOKEN)

MINI_APP_URL = "https://blackdot.dfa.media/?uuid={uuid}"

FRONT_URL = environ.get("FRONT_URL")

UNFOLD = {
    "SITE_TITLE": "Точка чёрного",
    "SITE_HEADER": "Администрирование",
    "SITE_URL": FRONT_URL,
    "SITE_SYMBOL": None,
    "SHOW_HISTORY": False,
    "SHOW_VIEW_ON_SITE": True,
    # "COLORS": {
    #     "primary": {
    #         "50": "32 128 216",
    #         "100": "32 128 216",
    #         "200": "32 128 216",
    #         "300": "32 128 216",
    #         "400": "32 128 216",
    #         "500": "32 128 216",
    #         "600": "32 128 216",
    #         "700": "32 128 216",
    #         "800": "32 128 216",
    #         "900": "32 128 216",
    #         "950": "32 128 216",
    #     },
    # },
}

LOCALE_PATHS = [
    BASE_DIR / "tpa_locale/" / "unfold",
]

PAYKEEPER_USER = environ.get("PAYKEEPER_USER")
PAYKEEPER_PASSWORD = environ.get("PAYKEEPER_PASSWORD")
PAYKEEPER_URL = environ.get("PAYKEEPER_URL")

VENDISTA_API_URL = environ.get("VENDISTA_API_URL")

YANDEX_GEOCODER_API_KEY = environ.get("YANDEX_GEOCODER_API_KEY")
