"""
Django settings for TripitakaPlatform project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _
import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2dx3sbj0#=4k$xu=8h52to&a2zia%%lr(w2h4wf$zb(ux6v9az'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'dmXadmin.apps.DmxadminConfig',
    'tdata.apps.TdataConfig',
    'tasks.apps.TasksConfig',
    'rect.apps.RectConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'django_extensions',
    'background_task',
    'corsheaders',
    'rest_framework',
    'jwt_auth',
    'django_celery_beat',
    'django_celery_results',
    'celery',
    'xadmin',
    'crispy_forms',
    'xapps',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    'TripitakaPlatform.jwt_auth_middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
#    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TripitakaPlatform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2'
        ,
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'TripitakaPlatform.jinja2.environment',
            # 'context_processors': [
            #     'django.template.context_processors.debug',
            #     'django.template.context_processors.request',
            #     'django.contrib.auth.context_processors.auth',
            #     'django.contrib.messages.context_processors.messages',
            # ],
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates'
        ,
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, "xapps/common/templates")]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': True,
        },
    },

]

WSGI_APPLICATION = 'TripitakaPlatform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tripitaka_platform',
        'USER': 'lqzj',
        'PASSWORD': 'lqdzjsql',
        #'HOST': '192.168.2.10'
        'HOST': 'localhost'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True
USE_TZ = False

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, 'xapps/common/static'),
]

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

IMAGE_URL_PREFIX = 'https://s3.cn-north-1.amazonaws.com.cn/lqdzj-image'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated', ),
    "DEFAULT_PAGINATION_CLASS": "ccapi.pagination.StandardPagination",
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': (
    'jwt_auth.authentication.JWTAuthentication',
    #'rest_framework.authentication.SessionAuthentication',
    'TripitakaPlatform.authentication.CsrfExemptSessionAuthentication',
    )
}

JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'jwt_auth.serializers.jwt_response_payload_handler',
    'JWT_PAYLOAD_HANDLER': 'jwt_auth.serializers.jwt_payload_handler',
    'JWT_AUTH_COOKIE': 'auth',
    'JWT_COOKIE_DOMAIN': 'lqdzj.cn',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=30),
}

AUTH_USER_MODEL='jwt_auth.Staff'

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    'lqdzj.cn',
    'localhost:8080',
    '127.0.0.1:8000'
)

CORS_ORIGIN_REGEX_WHITELIST = (r'^(https?://)?(\w+\.)?lqdzj\.cn$', )

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
#MEDIA_URL = '/media/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = '/www/cutrect/media'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
#STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# 当运行 python manage.py collectstatic 的时候
# STATIC_ROOT 文件夹 是用来将所有 STATICFILES_DIRS 中所有文件夹中的文件，以及各 app 中 static 中的文件都复制过来
# 把这些文件放到一起是为了用 apache/nginx 等部署的时候更方便
STATIC_ROOT = '/www/tripitaka_platform/static'

# Additional locations of static files
# STATICFILES_DIRS = (
#     # Put strings here, like "/home/html/static" or "C:/www/django/static".
#     # Always use forward slashes, even on Windows.
#     # Don't forget to use absolute paths, not relative paths.
# )
# Add for vuejs

# List of finder classes that know how to find static files in
# various locations.
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     'django.contrib.staticfiles.finders.DefaultStorageFinder',
# )


# Redis Cache Settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

# DEFAULT SESSION ENGINE IS 'django.contrib.sessions.backends.db'
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = "default"
# Redis Cache Settings end


#使用 supervisor 管理进程
#http://liyangliang.me/posts/2015/06/using-supervisor/
#Celery Tasks 参数介绍.
#http://www.jianshu.com/p/d8cbd4c72758

# 定制celery任务，使用AWS的SQS服务
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

CELERY_BROKER_USER = os.environ.get('AWS_ACCESS_KEY', '')
CELERY_BROKER_PASSWORD = os.environ.get('AWS_SECRET_KEY', '')

CELERY_BROKER_TRANSPORT = 'sqs'
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'polling_interval': 3,
    'region': 'cn-north-1',
    'visibility_timeout': 3600,
    'queue_name_prefix': 'lq-prod-'
}

# CELERY_WORKER_STATE_DB = '/var/run/celery/worker.db'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_WORKER_PREFETCH_MULTIPLIER = 0         # See https://github.com/celery/celery/issues/3712
#CELERY_RESULT_BACKEND = 'sqla+sqlite:///results.sqlite'
CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
CELERY_DEFAULT_QUEUE = 'lqcharacter_sqs'
CELERY_QUEUES = {
    CELERY_DEFAULT_QUEUE: {
        'exchange': CELERY_DEFAULT_QUEUE,
        'binding_key': CELERY_DEFAULT_QUEUE,
    }
}

CELERY_BROKER_CONNECTION_RETRY=False

CELERY_IMPORTS = (
        'TripitakaPlatform.celery_tasks',
    )

## 系统邮箱设置
EMAIL_HOST = 'smtp.sina.cn'
EMAIL_PORT = 25
EMAIL_HOST_USER = '17074810135@sina.cn'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PW', '')
EMAIL_USE_TLS = True
EMAIL_FROM = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000
