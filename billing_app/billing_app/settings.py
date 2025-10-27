"""
Django settings for billing_app project.
Updated for Railway deployment.
"""

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------------------------------------------------
# 🔐 SECURITY SETTINGS
# -------------------------------------------------------------------

# Secret key (read from environment for security)
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-dev-key")

# Debug mode (default False for production)
DEBUG = True

# Allowed hosts (Railway sets its own domain)
ALLOWED_HOSTS = ["panditofcodes.pythonanywhere.com", "127.0.0.1"]


# -------------------------------------------------------------------
# 🚀 APPLICATIONS
# -------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Custom apps
    "masters",
    "transactions",
    "printformats",
    'widget_tweaks',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Enable WhiteNoise for static files in production
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "billing_app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "billing_app" /"templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "billing_app.wsgi.application"


# -------------------------------------------------------------------
# 🗄️ DATABASE CONFIGURATION
# -------------------------------------------------------------------

# Default to SQLite (local) but override with Railway's DATABASE_URL
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=False,
    )
}


# -------------------------------------------------------------------
# 🔐 PASSWORD VALIDATION
# -------------------------------------------------------------------

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


# -------------------------------------------------------------------
# 🌍 INTERNATIONALIZATION
# -------------------------------------------------------------------

LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


# -------------------------------------------------------------------
# 🧾 STATIC & MEDIA FILES
# -------------------------------------------------------------------

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise compression & caching for Railway
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# -------------------------------------------------------------------
# 🧭 LOGIN/LOGOUT REDIRECTS
# -------------------------------------------------------------------

LOGIN_REDIRECT_URL = "dashboard"
LOGIN_URL = "login"
LOGOUT_REDIRECT_URL = "login"


# -------------------------------------------------------------------
# 🛠️ DEFAULT PRIMARY KEY
# -------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
