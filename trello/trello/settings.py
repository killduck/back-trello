import os

from dotenv import load_dotenv

from pathlib import Path



load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-g(yyp6r242twmylqjtrdm2p+m4y@)3qh!vnfx$175(@*n!2t7#"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG_STATUS = os.getenv('DEBUG_STATUS')

DEBUG = False if DEBUG_STATUS == 'False' else True


ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '147.45.185.171',
    'top-python31.ru'
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://top-python31.ru",
    "http://www.top-python31.ru",
    "https://top-python31.ru",
    "https://www.top-python31.ru",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",  # Подключаем библиотеку/приложение django-cors-headers
    "trello",
    "django_seed",
]


REST_FRAMEWORK = {
    # Разрешение на уровне проекта - все запросы только для авторизированным
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # регистрируйем обработчик CorsMiddleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "trello.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "trello.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    "default": {
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', default='trello'),
        'USER': os.getenv('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='123'),
        'HOST': os.getenv('DB_HOST', default='localhost'),
        'PORT': os.getenv('DB_PORT', default='5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

# LANGUAGE_CODE = "en-us"
LANGUAGE_CODE = "ru-ru"

# TIME_ZONE = "UTC"
TIME_ZONE = "Europe/Moscow"

USE_L10N = True

USE_I18N = True

USE_TZ = False  # при True глючит загрузка seedов модели User


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static_backend/'
STATIC_ROOT = BASE_DIR / 'static_backend'


# разрешаем обрабатывать запросы, приходящие с любого хоста, игнорируя политику Same Origin.
# При диплое на сервер установить False или удалите ключ CORS_ORIGIN_ALLOW_ALL
CORS_ORIGIN_ALLOW_ALL = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Переопределить параметр AUTH_USER_MODEL, который по умолчанию принимает значение 'auth.User'.
AUTH_USER_MODEL = 'trello.User'

# Общие настройки для админок
EMPTY_VALUE_DISPLAY = '-пусто-'


# Настройка почтового сервера
METHOD = {
    'smtp': 'django.core.mail.backends.smtp.EmailBackend',
    'console': 'django.core.mail.backends.console.EmailBackend',
    'file': 'django.core.mail.backends.filebased.EmailBackend'
}
EMAIL_BACKEND = ''
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.timeweb.ru'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'python31@top-python31.ru'
EMAIL_HOST_PASSWORD = 'Python31!'


# Настройки для сообщений
MAIL_MESSAGE = {
    'add_dashboard': f'Вас приглашают стать учаcтником доски. Пройдите по ссылке https://www.google.ru/#',
    'deadline': f'У вас просрочена задача ',
    'test': 'Тестовое сообщение/Test message!!!',
    'empty': '',
}
