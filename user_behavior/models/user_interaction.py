from django.db import models
from django.utils.translation import gettext_lazy as _

from user_behavior.models.helper.enum.event_type import EventType


class UserInteraction(models.Model):
    session = models.ForeignKey(
        to="UserSession",
        on_delete=models.CASCADE,
        verbose_name=_("User Session"),
        db_comment="The user session associated with this interaction.",
        help_text=_("The user session during which this interaction occurred."),
    )
    event_type = models.CharField(
        verbose_name=_("Event Type"),
        max_length=50,
        choices=EventType.choices,
        db_comment="Type of user interaction (e.g., click, scroll).",
        help_text=_("The type of interaction performed by the user."),
    )
    element = models.TextField(
        verbose_name=_("Element"),
        db_comment="The HTML element interacted with.",
        help_text=_(
            "The ID, class, or tag name of the element the user interacted with."
        ),
    )
    timestamp = models.DateTimeField(
        verbose_name=_("Timestamp"),
        auto_now_add=True,
        db_comment="Timestamp when the interaction occurred.",
        help_text=_("The time when the interaction occurred."),
    )
    metadata = models.JSONField(
        verbose_name=_("Metadata"),
        default=dict,
        db_comment="Additional data about the interaction (e.g., coordinates).",
        help_text=_("Extra metadata like mouse coordinates, scroll position, etc."),
        blank=True,
    )

    class Meta:
        verbose_name = _("User Interaction")
        verbose_name_plural = _("User Interactions")

    def __str__(self):
        return f"{self.event_type} on {self.element} at {self.timestamp}"
