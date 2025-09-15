import os
import sys
from pathlib import Path
from decouple import config as env  # avoid clashing with your config.py

# Import custom configuration module safely
sys.path.append(str(Path(__file__).resolve().parent.parent))
try:
    import config as app_config
except ImportError:
    app_config = None

# Safe fallbacks even if config.py exists but lacks keys
DATABASE_BACKEND   = getattr(app_config, 'DATABASE_BACKEND', 'sqlite')
APP_CONFIG         = getattr(app_config, 'APP_CONFIG', {'timezone': 'Asia/Bangkok', 'language_code': 'en-us'})
SECURITY_CONFIG    = getattr(app_config, 'SECURITY_CONFIG', {'debug_mode': True, 'allowed_hosts': ['*']})
get_database_config = getattr(app_config, 'get_database_config', lambda: {'database_path': 'db.sqlite3'})

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('SECRET_KEY', default='django-insecure-#x$x9qj_d_p4%1o16&t0-(==t%=z3muz($+=p1nzn##lpfhna=')
DEBUG = env('DEBUG', default=SECURITY_CONFIG.get('debug_mode', True), cast=bool)
ALLOWED_HOSTS = SECURITY_CONFIG.get('allowed_hosts', ['localhost', '127.0.0.1', '*'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'accounts',
    'booking',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',  # Temporarily disabled to fix CSRF errors
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    "classroom_booking.middleware.LoginRequiredMiddleware",  # Temporarily disabled
]

ROOT_URLCONF = 'classroom_booking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'classroom_booking.wsgi.application'

# Database Configuration based on config.py
if DATABASE_BACKEND == 'sqlite' or env('USE_SQLITE', default=True, cast=bool):
    # Development with SQLite
    sqlite_config = get_database_config() if 'get_database_config' in globals() else {'database_path': 'db.sqlite3'}
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / sqlite_config.get('database_path', 'db.sqlite3'),
        }
    }
elif DATABASE_BACKEND in ['postgresql', 'timescaledb']:
    # Production with PostgreSQL/TimescaleDB
    pg_config = get_database_config() if 'get_database_config' in globals() else {}
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DB_NAME', default=pg_config.get('database_name', 'classroom_booking')),
            'USER': env('DB_USER', default=pg_config.get('username', 'postgres')),
            'PASSWORD': env('DB_PASSWORD', default=pg_config.get('password', '')),
            'HOST': env('DB_HOST', default=pg_config.get('host', 'localhost')),
            'PORT': env('DB_PORT', default=str(pg_config.get('port', '5432'))),
            'OPTIONS': {
                'connect_timeout': pg_config.get('connection_timeout', 60),
            }
        }
    }
else:
    # Fallback to SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


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
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Login URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Session settings
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True

# JSON Data Storage
JSON_DATA_DIR = BASE_DIR / 'data'
if not os.path.exists(JSON_DATA_DIR):
    os.makedirs(JSON_DATA_DIR)

# Booking settings
BOOKING_TIME_SLOTS = [
    ('09:00', '09:00'),
    ('10:00', '10:00'),
    ('11:00', '11:00'),
    ('12:00', '12:00'),
    ('13:00', '13:00'),
    ('14:00', '14:00'),
    ('15:00', '15:00'),
    ('16:00', '16:00'),
    ('17:00', '17:00'),
]

BOOKING_MIN_HOURS = 1
BOOKING_MAX_HOURS = 4

# WhiteNoise settings for static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
