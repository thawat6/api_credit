from dataservice.settings.common import *

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "jumpvrp",
        "USER": "vrp",
        "PASSWORD": "1q2w3e4r",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = "/vrp/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

CORS_ORIGIN_WHITELIST = ("localhost:8000", "127.0.0.1:3000")
