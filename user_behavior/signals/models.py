import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from user_behavior.models import PageView, UserInteraction, UserSession

logger = logging.getLogger(__name__)


def log_event(instance, action):
    """Helper function to log model events."""
    logger.info("%s %s: %s", instance.__class__.__name__, action, instance)


@receiver(post_save, sender=UserSession)
@receiver(post_save, sender=PageView)
@receiver(post_save, sender=UserInteraction)
def log_create_update(sender, instance, created, **kwargs):
    """Log creation and update events."""
    action = "created" if created else "updated"
    log_event(instance, action)


@receiver(post_delete, sender=UserSession)
@receiver(post_delete, sender=PageView)
@receiver(post_delete, sender=UserInteraction)
def log_delete(sender, instance, **kwargs):
    """Log deletion events."""
    log_event(instance, "deleted")
