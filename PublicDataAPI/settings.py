from pathlib import Path
from datetime import timedelta
from decouple import config
import dj_database_url
import os
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load secret key from environment
SECRET_KEY = config('SECRET_KEY')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Set debug mode based on environment variable
DEBUG = config('DEBUG', default=False, cast=bool)

# Get the database URL from environment variable
DATABASE_URL = config('DATABASE_URL')  # Ensure DATABASE_URL is set in .env or environment

# Configure databases
DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=True)
}

# Allow all hosts
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',  # Required for Swagger
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.contract',
    'apps.public_api',
    'apps.utility',
    'apps.health',
    'drf_spectacular',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'PublicDataAPI.middleware.APIKeyMiddleware',  # Add API Key middleware
]


CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'PublicDataAPI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'PublicDataAPI.wsgi.application'

# Add API Key settings
API_KEY_HEADER = 'X-API-KEY'
API_KEY = config('API_KEY', default='your-default-api-key-here').strip('"\'')

# REST framework configuration for API Key authentication
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'PublicDataAPI.utils.custom_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'message',
}

PRODUCTION_URL = config('PRODUCTION_URL', default='https://default-url.app')
SPECTACULAR_SETTINGS = {
    'TITLE': 'Admin Dashboard API',
    'DESCRIPTION': '''
API documentation for the Admin Dashboard.

Authentication:
- All endpoints require an API key
- Add the API key in the X-API-KEY header
- Example: X-API-KEY: your-api-key-here
''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
        'displayOperationId': True,
    },
    'SERVERS': [
        {'url': PRODUCTION_URL, 'description': 'Production'},
        {'url': 'http://127.0.0.1:8000', 'description': 'Local Development'},
    ],
    'SECURITY': [{"ApiKeyAuth": []}],
    'SECURITY_DEFINITIONS': {
        'ApiKeyAuth': {
            'type': 'apiKey',
            'in': 'header',
            'name': API_KEY_HEADER,
            'description': f'API key must be provided in the {API_KEY_HEADER} header for all requests'
        }
    },
    'SERVE_AUTHENTICATION_CLASSES': [],
    'SERVE_PERMISSIONS_CLASSES': [],
    'SCHEMA_PATH_PREFIX': '/api/'
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FTP_ALLOW_OVERWRITE = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    'X-API-KEY',
]
