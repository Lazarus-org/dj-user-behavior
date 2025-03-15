from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserBehaviorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_behavior"
    verbose_name = _("Django User Behavior")

    def ready(self) -> None:
        """This method is called when the application is fully loaded.

        Its main purpose is to perform startup tasks, such as importing
        and registering system checks for validating the configuration
        settings of the app. It ensures that all necessary configurations
        are in place and properly validated when the Django project initializes.

        In this case, it imports the models signal to log events on the app models and
        imports the settings checks from the `user_behavior.settings` module to
        validate the configuration settings.

        """
        from user_behavior.settings import checks
        from user_behavior.signals import models
