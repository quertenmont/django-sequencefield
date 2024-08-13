import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "django-sequencefield"

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "tests",
]

INSTALLED_APPS += [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
]

MIDDLEWARE = [
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DATABASE", "postgres"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_SERVICE_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_SERVICE_PORT", "5432"),
        "OPTIONS": {
            "application_name": "django-test",
        },
    }
}
print("DEBUG DATABASE", DATABASES)

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

MEDIA_ROOT = os.path.join(BASE_DIR, "tests/media/")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "tests/static/")
STATIC_URL = "/static/"
