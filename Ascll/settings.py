"""
Django settings for Ascll project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
import firebase_admin
import base64
import json
from firebase_admin import credentials, db
from pcloud import PyCloud

# Replace with your pCloud email and password
email = 'suzanmarya@gmail.com'
password = str(os.environ.get("PCLOUD_PASSWORD"))

pc = PyCloud(email, password)

# Open the file on pCloud
response = pc.file_open(path=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"), flags=0x0040)  # 0x0040 is the flag for read access
file_descriptor = response['fd']

# Get the file size
size_response = pc.file_size(fd=file_descriptor)
file_size = size_response['size']

# Read the file content
file_content_response = pc.file_read(fd=file_descriptor, count=file_size)
file_content = file_content_response['data']

# Load the credentials from the file content
cred_dict = json.loads(file_content)

# Initialize Firebase Admin SDK
cred = credentials.Certificate(cred_dict)
if not firebase_admin._apps:  # Prevent re-initialization
    firebase_admin.initialize_app(cred)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wlqawk5zgtsm@wou&m9kq+lg%#z)mwx7gk(1qi_u#w2d=uuhs$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    # 'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'djoser',
    # 'dj_rest_auth',
    # 'django.contrib.sites',
    # 'allauth',
    # 'allauth.account',
    # 'dj_rest_auth.registration',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.twitter',
    # 'allauth.socialaccount.providers.google',
    'channels',
    "Chat",
]

# Configure the ASGI application
ASGI_APPLICATION = 'your_project_name.asgi.application'

# Redis settings (for channels_redis)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis-14980.c244.us-east-1-2.ec2.redns.redis-cloud.com', 14980)],  # Ensure Redis is running
            "password": "kaxP1S1Lwdoy0pvs95mv3688zwM03MnE"
        },
    },
}

# SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'Ascll.urls'

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

WSGI_APPLICATION = 'Ascll.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'railway',
    'USER': 'postgres',
    'PASSWORD': 'EEDnqMRuxBjpwgssfjWENuJzZbnARmkU',
    'HOST': 'metro.proxy.rlwy.net',
    'PORT': '23063',
}
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        "rest_framework.permissions.IsAuthenticated",
    ]
}

SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('JWT',),
}
