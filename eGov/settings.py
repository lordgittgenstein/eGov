import os

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'b-o_7bu!k-q=_-f*kql^cme&+y#-4@i9l3c_dcc_glph)_eop&'

CAPTCHA_TEST_MODE = True
CAPTCHA_OUTPUT_FORMAT = u'<span> %(image)s %(text_field)s </span> %(hidden_field)s'
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots',)
CAPTCHA_LETTER_ROTATION = (-10, 10)
CAPTCHA_FONT_SIZE = 25
CAPTCHA_FOREGROUND_COLOR = '#001100'

LIST_SIZE = 8
PAGE_WINDOW = 3
WAIT_DAYS = 21
MAX_HISTORY_SIZE = 128
HISTORY_PAD = 3


PATH_TO_SOURCE = '/home/ranbir/Workspace/eGov/'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = PATH_TO_SOURCE + 'media/'

STATICFILES_DIRS = (
    PATH_TO_SOURCE + 'static',
)

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'egov',
        'USER':     'root',
        'PASSWORD': 'bobono',
        'HOST':     'localhost',
        'PORT':     '3306',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'captcha',
    'corect',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'eGov.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ PATH_TO_SOURCE + 'templates' ],
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

WSGI_APPLICATION = 'eGov.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
