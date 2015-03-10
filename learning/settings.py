# coding=utf-8
"""
Django settings for blog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l+wd-ni8ofa7xz79_1-)^7!_e(p!@)nwlhu6nnkzc7^+%bzh%u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_markdown',
    'endless_pagination',
    'blog',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'learning.urls'

WSGI_APPLICATION = 'learning.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
from local_settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci'
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# media settings
MEDIA_ROOT = '/data/www/learning/media'
MEDIA_URL = "http://curvelearning.net/media/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/data/www/learning/static'
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), '../static').replace('\\','/'),
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), '../template').replace('\\', '/'),
)

# django-markdown settings
MARKDOWN_EXTENSIONS = ['extra', 'codehilite', 'meta', 'toc']
MARKDOWN_EXTENSION_CONFIGS = {}

# django-endless-pagination settings
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)
ENDLESS_PAGINATION_PER_PAGE = 8
ENDLESS_PAGINATION_PREVIOUS_LABEL = '&larr;上一页'
ENDLESS_PAGINATION_NEXT_LABEL = '下一页 &rarr;'

# baidu ping
BAIDU_PING_SERVICE = "http://ping.baidu.com/ping/RPC2"
SITE_URL = "http://curvelearning.net"
SITE_NAME = "学习小站 - 技术学习与思考"