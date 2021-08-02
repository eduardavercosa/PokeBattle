from .base import *  # noqa


DEBUG = True

HOST = "http://localhost:8000"

SECRET_KEY = "secret"

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": base_dir_join("db.sqlite3"),}
}

STATIC_ROOT = base_dir_join("staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = base_dir_join("mediafiles")
MEDIA_URL = "/media/"

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

AUTH_PASSWORD_VALIDATORS = []  # allow easy passwords only on local

# Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_BROKER_URL = 'redis://:p473426053d946140da1c86201ec599075b4e2a713889ea68e543d70da24bd984@ec2-44-194-75-243.compute-1.amazonaws.com:28839'
CELERY_RESULT_BACKEND = 'redis://:p473426053d946140da1c86201ec599075b4e2a713889ea68e543d70da24bd984@ec2-44-194-75-243.compute-1.amazonaws.com:28839'

# Email
INSTALLED_APPS += ("naomi",)
EMAIL_BACKEND = "naomi.mail.backends.naomi.NaomiBackend"
EMAIL_FILE_PATH = base_dir_join("tmp_email")


# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"standard": {"format": "%(levelname)-8s [%(asctime)s] %(name)s: %(message)s"},},
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "standard",},
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "INFO"},
        "celery": {"handlers": ["console"], "level": "INFO"},
    },
}

JS_REVERSE_JS_MINIFY = False
