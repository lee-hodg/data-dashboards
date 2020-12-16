"""
Production settings
"""
from .base import *

DEBUG = False

# TODO: add real domain
# Production site ID
SITE_ID = 1
SITE_CONFIG = {
    'name': 'Data Dashboard',
    'domain': 'data-dashboards.logicon.io'
}


ALLOWED_HOSTS = [
    'data-dashboards.logicon.io',
]
