from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserBehaviorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_behavior"
    verbose_name = _("Django User Behavior")


    def ready(self):
        import user_behavior.signals.models
