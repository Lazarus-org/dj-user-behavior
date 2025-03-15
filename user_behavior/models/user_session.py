from django.db import models
from django.utils.translation import gettext_lazy as _


class UserSession(models.Model):
    session_id = models.CharField(
        verbose_name=_("Session ID"),
        max_length=255,
        unique=True,
        db_comment="Unique identifier for the user session.",
        help_text=_("A unique ID generated for each user session."),
    )
    user_agent = models.TextField(
        verbose_name=_("User Agent"),
        db_comment="User agent string of the user's browser.",
        help_text=_(
            "The user agent string helps identify the browser and device used."
        ),
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_("IP Address"),
        db_comment="IP address of the user.",
        help_text=_("The IP address from which the session originated."),
    )
    start_time = models.DateTimeField(
        verbose_name=_("Start Time"),
        auto_now_add=True,
        db_comment="Timestamp when the session started.",
        help_text=_("The time when the user session began."),
    )
    end_time = models.DateTimeField(
        verbose_name=_("End Time"),
        null=True,
        blank=True,
        db_comment="Timestamp when the session ended.",
        help_text=_("The time when the user session ended."),
    )
    user_id = models.CharField(
        verbose_name=_("User ID"),
        max_length=255,
        null=True,
        blank=True,
        db_comment="Optional identifier for the user (e.g., logged-in user ID).",
        help_text=_("If the user is logged in, this field stores their unique ID."),
    )

    class Meta:
        verbose_name = _("User Session")
        verbose_name_plural = _("User Sessions")

    def __str__(self):
        return f"Session {self.session_id} - User ID: ({self.user_id})"
