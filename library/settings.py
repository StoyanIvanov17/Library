import os
from pathlib import Path

from django.urls import reverse_lazy
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', config('SECRET_KEY'))

DEBUG = os.getenv('DEBUG', config('DEBUG')) == "True"

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', config('ALLOWED_HOSTS')).split(',')

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', config('CSRF_TRUSTED_ORIGINS', [])).split(',')

PROJECT_MADE_APPS = [
    'library.lb_accounts',
    'library.lb_collections',
    'library.lb_events',
    'library.lb_home',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + PROJECT_MADE_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'library.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'library.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv('DB_NAME', config('DB_NAME')),
        "USER": os.getenv('DB_USER', config('DB_USER')),
        "PASSWORD": os.getenv('DB_PASS', config('DB_PASSWORD')),
        "HOST": os.getenv('DB_HOST', config('DB_HOST')),
        "PORT": os.getenv('DB_PORT', config('DB_PORT')),
    }
}

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

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_ROOT = BASE_DIR / 'mediafiles'
MEDIA_URL = '/media/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'lb_accounts.LibraryUser'

LOGIN_REDIRECT_URL = 'registration profile'
LOGIN_URL = 'signin user'
LOGOUT_REDIRECT_URL = 'home page'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', config('EMAIL_HOST'))
EMAIL_PORT = os.getenv('EMAIL_PORT', config('EMAIL_PORT'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', config('EMAIL_USE_TLS')) == "True"
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', config('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', config('EMAIL_HOST_PASSWORD'))
