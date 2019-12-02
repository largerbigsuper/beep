"""
Base settings to build other settings files upon.
"""

import environ

from .settings_ckeditor import *
from .settings_beep import *

ROOT_DIR = (
    environ.Path(__file__) - 3
)  # (beep/config/settings/base.py - 3 = beep/)
APPS_DIR = ROOT_DIR.path("beep")

env = environ.Env()

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "Asia/Shanghai"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
# USE_TZ = True
USE_TZ = False



# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
]
THIRD_PARTY_APPS = [
    "rest_framework",
    'rest_framework.authtoken',
    "crispy_forms",
    "django_filters",
    "drf_yasg",
    "channels",
    'ckeditor',
    'ckeditor_uploader',
]

LOCAL_APPS = [
    "beep.users",
    "beep.common",
    "beep.activity",
    "beep.blog",
    "beep.news",
    "beep.search",
    "beep.wechat_callback",
    "beep.wechat",
    "beep.ad",
    "beep.cfg",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS



# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    # "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR("static"))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
# STATICFILES_DIRS = [str(ROOT_DIR.path("static"))]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
# STATICFILES_FINDERS = [
#     "django.contrib.staticfiles.finders.FileSystemFinder",
#     "django.contrib.staticfiles.finders.AppDirectoriesFinder",
# ]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(ROOT_DIR("media"))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(ROOT_DIR.path("templates"))],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
# SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
# CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
# https://docs.djangoproject.com/en/2.2/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
LOGIN_URL = "api-auth/login/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""frankie""", "admin@beep.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

INSTALLED_APPS += ["compressor"]
# STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]
# Your stuff...
# ------------------------------------------------------------------------------

AUTH_USER_MODEL = 'users.User'


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.CustomPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'utils.render.FormatedJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),

    'TEST_REQUEST_DEFAULT_FORMAT': 'json',

    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',

    'DATETIME_INPUT_FORMATS': [
        '%Y-%m-%d %H:%M:%S',  # '2006-10-25 14:30:59'
        '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
        '%Y-%m-%d %H:%M',  # '2006-10-25 14:30'
        '%Y-%m-%d',  # '2006-10-25'
        '%m/%d/%Y %H:%M:%S',  # '10/25/2006 14:30:59'
        '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
        '%m/%d/%Y %H:%M',  # '10/25/2006 14:30'
        '%m/%d/%Y',  # '10/25/2006'
        '%m/%d/%y %H:%M:%S',  # '10/25/06 14:30:59'
        '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
        '%m/%d/%y %H:%M',  # '10/25/06 14:30'
        '%m/%d/%y',  # '10/25/06'
    ]
}

# Django 
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# Storage
DEFAULT_FILE_STORAGE = 'utils.qiniucloud.StorageObject'

# ALL SETTINGS MAST BE UPPERCASE

# MINI_PROGRAM_APP_ID = 'wx1743dc274cf46871'
# MINI_PROGRAM_APP_SECRET = '648a7ae2cbf66aa7e48992d76f46e621'

MINI_PROGRAM_APP_ID = 'wx300f2f1d32b30613'
MINI_PROGRAM_APP_SECRET = '2d6b9fef49827381af8dd26b4b66f5e5'
MINI_PROGRAM_LOGIN_URL = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&grant_type=userization_code&js_code='.format(MINI_PROGRAM_APP_ID, MINI_PROGRAM_APP_SECRET)
MINI_PROGRAM_ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(MINI_PROGRAM_APP_ID, MINI_PROGRAM_APP_SECRET)

WX_WEB_APP_ID = 'wx69969d53697f5fdb'
WX_WEB_APP_SECRET = '7b571b1b70c7329e7f87a4e5147a7241'
# WX_WEB_APP_REDIRECT_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&grant_type=authorization_code&code='.format(WX_WEB_APP_ID, WX_WEB_APP_SECRET)
WX_WEB_APP_ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&grant_type=authorization_code&code='.format(WX_WEB_APP_ID, WX_WEB_APP_SECRET)
WX_USER_INFO_URL = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}'


QINIU_ACCESS_KEY = 'r9Wn86UUlqWqRbt1E4Mvl8lPXPcZpSSH1t2n0MR6'
QINIU_SECRET_KEY = 'OdRXdCnUSpDdkY5n4-PUQT3psAm2zJMiHvgNfU_S'
QINIU_BUCKET_NAME_DICT = {
    'image': 'images-beepcrypto',
    'video': 'videos-beepcrypto'
}
QINIU_BUCKET_DOMAIN_DICT = {
    'image': 'https://cdn.beepcrypto.com/',
    'video': 'https://cdn.beepcrypto.com/'
}

# jieba分词
# import jieba
# JIEBA = jieba
# JIEBA.initialize()
# JIEBA_WORD_PATH = ROOT_DIR.path('config/jieba.txt')
# with open(JIEBA_WORD_PATH) as f:
#     for word in f.readlines():
#         JIEBA.add_word(word)


import pathlib
LOG_ROOT = APPS_DIR = ROOT_DIR.path("logs")

pathlib.Path(LOG_ROOT).mkdir(parents=True, exist_ok=True)

LOG_LEVEL_DEBUG = 'DEBUG'
LOG_LEVEL_INFO = 'INFO'
LOG_LEVEL_WARNING = 'WARNING'
LOG_LEVEL_ERROR = 'ERROR'
LOG_LEVEL_CRITICAL = 'CRITICAL'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            # 'filters': ['special']
        },
        "django_file": {
            "level": LOG_LEVEL_INFO,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./logs/access.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 10,
            "formatter": "verbose"
        },
        "request_file": {
            "level": LOG_LEVEL_INFO,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./logs/requests.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 10,
            "formatter": "verbose"
        },
        "wehub_file": {
            "level": LOG_LEVEL_INFO,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./logs/wehub.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 10,
            "formatter": "verbose"
        },
        "qiniu_file": {
            "level": LOG_LEVEL_INFO,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./logs/qiniu.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 10,
            "formatter": "verbose"
        },
        "cornjob_file": {
            "level": LOG_LEVEL_INFO,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./logs/cornjob_file.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 10,
            "formatter": "verbose"
        },
        "api_weixin_file": {
            "level": LOG_LEVEL_INFO,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./logs/api_weixin.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 10,
            "formatter": "verbose"
        },
        "api_error_file": {
            "level": LOG_LEVEL_WARNING,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./logs/api_error.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 10,
            "formatter": "verbose"
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'django_file', 'mail_admins'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['request_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'wehub': {
            'handlers': ['wehub_file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'qiniu': {
            'handlers': ['qiniu_file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'cornjob': {
            'handlers': ['cornjob_file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'api_weixin': {
            'handlers': ['api_weixin_file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'api_error': {
            'handlers': ['api_error_file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

ASGI_APPLICATION = 'config.routing.application'
# 图片上传限制
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1000
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1000