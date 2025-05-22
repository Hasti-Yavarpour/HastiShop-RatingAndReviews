from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # ✅ Database engine
        'NAME': BASE_DIR / "db.sqlite3",  # ✅ Database file
    }
}
INSTALLED_APPS = [
    'django.contrib.admin',      # ✅ Admin panel
    'django.contrib.auth',       # ✅ User authentication
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'shop',  # Your app (Make sure this is added)
]


DEBUG = True  # Ensure this is True for development

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
ROOT_URLCONF = 'HastiShop.urls'

import os

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # This makes Django look in your /static folder
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Only used in production

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
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # ✅ Required for Admin Panel
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ✅ Required for Authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # ✅ Required for Admin Messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



SECRET_KEY = 'dA74i2hw7QOpeWftduiG0ba7tgtYKao4z9VXMJQy7mwKZeIFYzrIJpjX1YPtk2qp7L0'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your@email.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # NOT your normal password!

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMINS = [('Admin', 'your@email.com')]

