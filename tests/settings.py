DEBUG = True
SECRET_KEY = "django-markup-tests"

INSTALLED_APPS = (
    "django_markup",
)

TEMPLATES = (
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    },
)
