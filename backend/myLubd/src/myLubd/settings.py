"""
Django settings for myLubd project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent




# Security
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-default-secret-key')
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'  # Default to False for security

# Hosts and Security Settings
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    
    '[::1]',
    'pmcs.site',
    'www.pmcs.site',
    'django-backend',
    
     'backend',
       # Temporarily add this for debugging
]
# Google OAuth Settings
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

# OAuth2 settings
OAUTH2_SETTINGS = {
    'GOOGLE': {
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://oauth2.googleapis.com/token',
        'userinfo_uri': 'https://www.googleapis.com/oauth2/v3/userinfo',
    }
}

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'myappLubd',
    'corsheaders',
    'debug_toolbar',
    'rest_framework_simplejwt',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Move this up
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
   
]

# URLs and WSGI
ROOT_URLCONF = 'myLubd.urls'
WSGI_APPLICATION = 'myLubd.wsgi.application'

# Templates
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

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mylubd_db',
        'USER': 'mylubd_user',
        'PASSWORD': 'Sqreele1234#',
        'HOST': 'db',
        'PORT': '5432',
    }
}

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # Remove SessionAuthentication if you're only using JWT
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# CORS and CSRF

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Static and Media Files
STATIC_URL = '/static/'
STATIC_ROOT = '/app/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media'
# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'WARNING',
    },
    'django': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'ERROR',
        'propagate': False,
    },
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_TZ = True

# Default Primary Key Field Type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# File Uploads
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
     "https://pmcs.site",
    "https://www.pmcs.site",
   "http://nextjs-frontend:3000",
    
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
      "https://pmcs.site",
    "https://www.pmcs.site",
    "http://nextjs-frontend:3000",
     
]
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']

# Add these CORS settings

CORS_ORIGIN_ALLOW_ALL = False
CORS_PREFLIGHT_MAX_AGE = 86400
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB in bytes
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760
