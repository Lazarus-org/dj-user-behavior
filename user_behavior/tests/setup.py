import django
from django.conf import settings
from django.core.management.utils import get_random_secret_key


def configure_django_settings() -> None:
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            SECRET_KEY=get_random_secret_key(),  # Add a secret key for testing
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                }
            },
            INSTALLED_APPS=[
                "django.contrib.admin",
                "django.contrib.auth",
                "django.contrib.contenttypes",
                "django.contrib.sessions",
                "django.contrib.messages",
                "django.contrib.staticfiles",
                "rest_framework",
                "user_behavior",
            ],
            MIDDLEWARE=[
                "django.middleware.security.SecurityMiddleware",
                "django.contrib.sessions.middleware.SessionMiddleware",
                "django.middleware.common.CommonMiddleware",
                "django.middleware.csrf.CsrfViewMiddleware",
                "django.contrib.auth.middleware.AuthenticationMiddleware",
                "django.contrib.messages.middleware.MessageMiddleware",
                "django.middleware.clickjacking.XFrameOptionsMiddleware",
            ],
            ROOT_URLCONF="user_behavior.tests.urls",
            USER_BEHAVIOR_API_PAGE_VIEW_FILTERSET_CLASS="user_behavior.api.filters.PageViewFilter",
            USER_BEHAVIOR_API_USER_SESSION_FILTERSET_CLASS="user_behavior.api.filters.UserSessionFilter",
            USER_BEHAVIOR_API_USER_INTERACTION_FILTERSET_CLASS="user_behavior.api.filters.UserInteractionFilter",
            LANGUAGE_CODE="en-us",
            TIME_ZONE="UTC",
            USE_I18N=True,
            USE_TZ=True,
        )
        django.setup()


configure_django_settings()
