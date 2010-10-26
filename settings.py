# Django settings for djkeptar project.
import os.path
PROJECT_DIR = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_DIR, 'keptar.sqlite'), # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Budapest'

LANGUAGE_CODE = 'hu'

SITE_ID = 1

USE_I18N = False
USE_L10N = False

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = 'r%at(19zx12aa7r9=0l&dmi2tj=ll1b&rx4_m46_^tf2)18q72'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'djkeptar.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'south',
    'taggit',
    'disqus',
    'keptar',
)

DISQUS_API_KEY = '201YglHp50UQB1gK50Um0UMRIGwlaSGqjUce1YRVVB43L0GRQcFE0Trt3zCHTTCA'
DISQUS_WEBSITE_SHORTNAME = 'djkeptar-dyuri'
KEPTAR_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, 'images'))
KEPTAR_URL = '/images/'
KEPTAR_EXTENSIONS = ['jpg','jpeg','png']
KEPTAR_THUMBS = {
        '': { 'dir': '.tn', 'size': (120,120) },
        'blog': { 'dir': '.tn/blog', 'size': (600,600) },
        }
KEPTAR_SHOW_HIDDEN = False
KEPTAR_ICONS = {
        'dir': '/media/keptar/icons/tn_dir.jpg',
        }

