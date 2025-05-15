# django_app/settings.py

from pathlib import Path
from django_app.__shared.config import ConfigService

import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

config = ConfigService()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.DEBUG

ALLOWED_HOSTS = config.ALLOWED_HOSTS

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.gis',
    'django_extensions',
    'django_filters',

    'corsheaders',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    'django_rest_passwordreset',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'schema_viewer',
    'django_dbml',

    'django_app.modules.v1.auth',
    'django_app.modules.v1.users',
    'django_app.modules.v1.places',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# django.contrib.sites
SITE_ID = 1

ROOT_URLCONF = 'django_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'django_app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': config.DATABASE_CONFIG
}

AUTH_USER_MODEL = 'users.User'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from datetime import timedelta

# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # 'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        "rest_framework_simplejwt.authentication.JWTAuthentication", # Use this to allow only Authorization Header
    ],
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = config.CORS_ALLOW_ALL_ORIGINS
CORS_ALLOWED_ORIGINS = config.CORS_ALLOWED_ORIGINS

# REST Auth settings
REST_AUTH = {
    "USE_JWT": True,
    # Name of access token cookie, remove this setting if you don't want access token to be sent as cookie
    # "JWT_AUTH_COOKIE": "_auth",
    # Name of refresh token cookie, remove this setting if you don't want refresh token to be sent as cookie
    # "JWT_AUTH_REFRESH_COOKIE": "_refresh",
    "JWT_AUTH_HTTPONLY": False,  # Makes sure refresh token is sent
    "PASSWORD_RESET_USE_SITES_DOMAIN": config.PASSWORD_RESET_USE_SITES_DOMAIN,
    'PASSWORD_RESET_SERIALIZER': 'django_app.modules.v1.auth.serializers.CustomPasswordResetSerializer'
}

RESET_PASSWORD_REDIRECT_URL = config.RESET_PASSWORD_REDIRECT_URL

# JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=config.JWT_ACCESS_TOKEN_LIFETIME_MINUTES),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=config.JWT_REFRESH_TOKEN_LIFETIME_DAYS),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": config.JWT_ALGORITHM,
    "SIGNING_KEY": config.JWT_SECRET_KEY,
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
}

# Allauth settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_EMAIL_VERIFICATION = config.ACCOUNT_EMAIL_VERIFICATION
ACCOUNT_AUTHENTICATED_REMEMBER = config.ACCOUNT_AUTHENTICATED_REMEMBER
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = config.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS
ACCOUNT_DEFAULT_HTTP_PROTOCOL = config.ACCOUNT_DEFAULT_HTTP_PROTOCOL
ACCOUNT_EMAIL_SUBJECT_PREFIX = config.ACCOUNT_EMAIL_SUBJECT_PREFIX
ACCOUNT_PASSWORD_MIN_LENGTH = config.ACCOUNT_PASSWORD_MIN_LENGTH
ACCOUNT_CONFIRM_EMAIL_ON_GET = config.ACCOUNT_CONFIRM_EMAIL_ON_GET

# Allauth sign up fields (added explicitly as required)
ACCOUNT_SIGNUP_FIELDS = config.ACCOUNT_SIGNUP_FIELDS
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = config.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = config.ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL

LOGIN_REDIRECT_URL = config.LOGIN_REDIRECT_URL
LOGOUT_REDIRECT_URL = config.LOGOUT_REDIRECT_URL

LOGIN_URL = config.FRONTEND_URL

# Django SMTP
EMAIL_BACKEND = config.EMAIL_BACKEND
EMAIL_HOST = config.EMAIL_HOST
EMAIL_PORT = config.EMAIL_PORT
EMAIL_USE_TLS = config.EMAIL_USE_TLS
EMAIL_HOST_USER = config.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = config.DEFAULT_FROM_EMAIL

# Frontend URL
FRONTEND_URL = config.FRONTEND_URL
