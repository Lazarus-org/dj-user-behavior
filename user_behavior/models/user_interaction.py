from django.db import models
from django.utils.translation import gettext_lazy as _

from .user_session import UserSession

class UserInteraction(models.Model):
    EVENT_TYPES = [
        ("click", _("Click")),
        ("scroll", _("Scroll")),
        ("mouse_move", _("Mouse Move")),
        ("form_submit", _("Form Submit")),
        ("input_change", _("Input Change")),
        ("page_resize", _("Page Resize")),
        ("keypress", _("Key Press")),
        ("hover", _("Hover")),
    ]

    session = models.ForeignKey(
        UserSession,
        on_delete=models.CASCADE,
        db_comment=_("The session associated with this interaction."),
        help_text=_("The session during which this interaction occurred.")
    )
    event_type = models.CharField(
        max_length=50,
        choices=EVENT_TYPES,
        db_comment=_("Type of user interaction (e.g., click, scroll)."),
        help_text=_("The type of interaction performed by the user.")
    )
    element = models.TextField(
        db_comment=_("The HTML element interacted with."),
        help_text=_("The ID, class, or tag name of the element the user interacted with.")
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_comment=_("Timestamp when the interaction occurred."),
        help_text=_("The time when the interaction occurred.")
    )
    metadata = models.JSONField(
        default=dict,
        db_comment=_("Additional data about the interaction (e.g., coordinates)."),
        help_text=_("Extra metadata like mouse coordinates, scroll position, etc.")
    )

    class Meta:
        db_table = "user_interactions"
        verbose_name = _("User Interaction")
        verbose_name_plural = _("User Interactions")

    def __str__(self):
        return f"{self.event_type} on {self.element} at {self.timestamp}"