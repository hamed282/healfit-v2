from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv
load_dotenv(override=True)


# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY KEY
SECRET_KEY = os.getenv('SECRET_KEY')


# Debug Mode
DEBUG = True

if DEBUG:
    ALLOWED_HOSTS = ['*']
    # ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'api.healfit.ae', 'www.api.healfit.ae', 'healfit.ae']

    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': BASE_DIR / 'db.sqlite3',
    #     }
    # }

    # Ensure the default charset is UTF-8
    DEFAULT_CHARSET = 'utf-8'

    # Ensure the default encoding for template rendering is UTF-8
    FILE_CHARSET = 'utf-8'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('NAME'),
            'USER': os.getenv('USER'),
            'PASSWORD': os.getenv('PASSWORD'),
            'HOST': os.getenv('HOST'),
            'PORT': os.getenv('PORT'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }
    CORS_ORIGIN_ALLOW_ALL = True
    # CORS_ALLOWED_ORIGINS = [
    #     'https://healfit.ae',  # دامنه فرانت‌اند شما
    # ]
    CORS_ALLOW_CREDENTIALS = True

else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'api.healfit.ae', 'www.api.healfit.ae', 'healfit.ae']

    DEFAULT_CHARSET = 'utf-8'
    FILE_CHARSET = 'utf-8'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('NAME'),
            'USER': os.getenv('USER'),
            'PASSWORD': os.getenv('PASSWORD'),
            'HOST': os.getenv('HOST'),
            'PORT': os.getenv('PORT'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }

    # CSRF_TRUSTED_ORIGINS = ['https://api.healfit.ae', 'https://*.127.0.0.1']
    CORS_ORIGIN_ALLOW_ALL = True
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'rest_framework',
    'django_celery_beat',
    'storages',
    'django_filters',
    'django.contrib.sitemaps',
    'dbbackup',
    'django_rest_passwordreset',

    # Installed App
    'accounts.apps.AccountsConfig',
    'admin_panel.apps.AdminPanelConfig',
    'blog.apps.BlogConfig',
    'product.apps.ProductConfig',
    'home.apps.HomeConfig',
    'order.apps.OrderConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

ROOT_URLCONF = 'A.urls'

WSGI_APPLICATION = 'A.wsgi.application'


# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dubai'
USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}


# Simple JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=90),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=180),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
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
    "SLIDING_TOKEN_LIFETIME": timedelta(days=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",

}


# Cart
CART_SESSION_ID = 'cart'


# Zoho Config
ORGANIZATION_ID = os.getenv('ORGANIZATION_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
GRANT_TYPE = os.getenv('GRANT_TYPE')
SCOPE_READING = os.getenv('SCOPE_READING')
SCOPE_UPDATE = os.getenv('SCOPE_UPDATE')
SCOPE_BOOK_CONTACTS = os.getenv('SCOPE_BOOK_CONTACTS')
SCOPE_BOOK_INVOICE = os.getenv('SCOPE_BOOK_INVOICE')
SCOPE_BOOK_TAX = os.getenv('SCOPE_BOOK_TAX')
SIOD = os.getenv('SIOD')


# Google Login
GOOGLE_CLIENT_ID = '404588717147-739as16dm0mu3n6u3un0d45f99qefmov.apps.googleusercontent.com'  # os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = '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'  # os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = 'https://healfit.ae/login/'  # os.getenv('GOOGLE_REDIRECT_URI')


# Apple Login
APPLE_KEY_ID = ''
APPLE_CLIENT_ID = ''
APPLE_TEAM_ID = ''
APPLE_PRIVATE_KEY = ''


# AWS Storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_ACCESS_KEY_ID = os.getenv('ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('SECRET_KEY')
AWS_S3_ENDPOINT_URL = os.getenv('ENDPOINT_URL')
AWS_STORAGE_BUCKET_NAME = os.getenv('BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_SIGNATURE_VERSION = os.getenv('AWS_S3_SIGNATURE_VERSION')


# TELR Settings
TELR_API_REQUEST = f"https://secure.telr.com/gateway/order.json"
TELR_API_VERIFY = f"https://secure.telr.com/gateway/order.json"
TEST = "0"
FRAMED = 0
SOTRE_ID = os.getenv('SOTRE_ID')
AUTHKEY = os.getenv('AUTHKEY')
CURRENCY = "AED"
AUTHORIZED_URL = "https://healfit.ae/success-pay"  # "https://rest.healfit.ae/api/order/authorised/"
DECLINED_URL = "https://healfit.ae/unsuccess-pay"  # "https://rest.healfit.ae/api/order/declined/"
CANCELLED_URL = "https://healfit.ae/cancel-pay-pay"  # "https://rest.healfit.ae/api/order/cancelled/"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.healfit.ae'
EMAIL_HOST_USER = 'no-reply@healfit.ae'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False


# DB Backup Storage
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {
    'location': '/home/healfita/backup/',
}
# DBBACKUP_CRYPT_ENABLED = True
# DBBACKUP_CRYPT_SECRET = 'your-encryption-secret-key'
# DBBACKUP_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# DBBACKUP_STORAGE_OPTIONS = {
#     'access_key': os.getenv('ACCESS_KEY'),
#     'secret_key': os.getenv('SECRET_KEY'),
#     'bucket_name': os.getenv('BUCKET_NAME'),
#     'region_name': os.getenv('AWS_S3_REGION_NAME'),
# }


# Tabby Payment Settings
TABBY_API_KEY = os.getenv('TABBY_API_KEY')
TABBY_MERCHANT_CODE = os.getenv('TABBY_MERCHANT_CODE')
SITE_URL = os.getenv('SITE_URL')
SITE_NAME = os.getenv('SITE_NAME')
FRONTEND_URL = os.getenv('FRONTEND_URL')

