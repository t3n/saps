import os
import environ
import psycopg2
from django.utils.crypto import get_random_string

BASE_DIR = environ.Path(__file__) - 2
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, get_random_string(length=50)),
    SITE_ID=(int, 1),
    SIPGATE_CLIENT_ID=(str, "dummy"),
    SIPGATE_CLIENT_SECRET=(str, "dummy"),
    PG_DB_NAME=(str, "saps"),
    PG_DB_HOST=(str, "localhost"),
    PG_DB_PORT=(int, 5432),
    PG_DB_PASS=(str, "saps"),
    PG_DB_USER=(str, "saps"),
)
environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

SITE_ID = env("SITE_ID")

SIPGATE_CLIENT_ID = env("SIPGATE_CLIENT_ID")

SIPGATE_CLIENT_SECRET = env("SIPGATE_CLIENT_SECRET")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]

AUTHLIB_OAUTH_CLIENTS = {
    "sipgate": {
        "client_id": env("SIPGATE_CLIENT_ID"),
        "client_secret": env("SIPGATE_CLIENT_SECRET"),
    }
}

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "behave_django",
    "saps",
    "sipgate",
    "snom",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "saps.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates"),],
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

WSGI_APPLICATION = "saps.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("PG_DB_NAME"),
        "USER": env("PG_DB_USER"),
        "PASSWORD": env("PG_DB_PASS"),
        "HOST": env("PG_DB_HOST"),
        "PORT": env("PG_DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
