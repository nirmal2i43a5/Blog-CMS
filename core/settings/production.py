import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

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





sentry_sdk.init(
    dsn="https://a7fa2149b3fa40aa9bbfc28c698d2c8c@o1109161.ingest.sentry.io/6137371",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)