"""
Development settings
"""
from .base import *

DEBUG = True

ALLOWED_HOSTS = []

WERKZEUG_DEBUG_PIN = 'off'
os.environ['WERKZEUG_DEBUG_PIN'] = WERKZEUG_DEBUG_PIN

INSTALLED_APPS += (
    'django_extensions',
)

# Django debug toolbar things

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

# Want this early if we are going to use it, but after static files
stat_files_idx = INSTALLED_APPS.index('django.contrib.staticfiles')
if DEBUG:
    INSTALLED_APPS.insert(stat_files_idx+1, 'debug_toolbar')

# Debug toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

# This is the site id for development environments.
SITE_ID = 3

# Site config for local development.
SITE_CONFIG = {
    'name': 'development',
    'domain': 'localhost'
}

ALLOWED_HOSTS = ['*']


log_conf = {'handlers': ['console'],
            'level': 'DEBUG'}
LOGGING['loggers'].update({'covid': log_conf})
LOGGING['formatters']['verbose']['()'] = 'coloredlogs.ColoredFormatter'

