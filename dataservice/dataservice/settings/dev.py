# -*- coding: utf-8 -*-
from dataservice.settings.common import *

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/vrp/static/'
#STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

CORS_ORIGIN_WHITELIST = ('http://localhost:8000', 'http://127.0.0.1:3000',
                         'http://0.0.0.0:8000')
