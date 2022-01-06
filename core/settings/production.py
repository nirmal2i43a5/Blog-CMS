# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

from .base import *


DEBUG = False

ALLOWED_HOSTS = [
                        'localhost',
                        '64.227.132.209',
                      'studybetterways.com',
                      'www.studybetterways.com'
          
             ]

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }