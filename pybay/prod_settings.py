import os
from pybay.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
EMAIL_DEBUG = DEBUG

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        'OPTIONS': {
            'read_default_file': '/home/pybay/pybay_prod.cnf',
            'charset': 'utf8mb4',
        },
    }
}

ALLOWED_HOSTS = ['pybay.com']

TIME_ZONE = "US/Pacific"

MEDIA_ROOT = '/data/websites/prod_site_media/media'
MEDIA_URL = "/site_media/media/"

STATIC_ROOT = '/data/websites/prod_site_media/static'
STATIC_URL = "/site_media/static/"

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# Add a filehandler for logging
LOGGING['handlers']['filelog'] = {
  'level': 'DEBUG',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': '/data/websites/logs/prod.log',
  'backupCount': 5,
  'maxBytes': 1024 * 1024 * 3,
  'formatter': 'verbose',
}

# Hook filehandler to django.request so we see 500 server errors in the file
LOGGING['loggers']['django.request']['handlers'].append('filelog')
# And also turn on for log.debug and up calls in pybay.* code
LOGGING['loggers']['pybay'] = {
  'handlers': ['filelog'],
  'level': 'DEBUG',
  'propagate': True,
}
