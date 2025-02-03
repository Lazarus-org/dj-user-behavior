# tracker/models.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .user_session import UserSession

class PageView(models.Model):
    session = models.ForeignKey(
        UserSession,
        on_delete=models.CASCADE,
        db_comment=_("The session associated with this page view."),
        help_text=_("The session during which this page view occurred.")
    )
    url = models.URLField(
        db_comment=_("The URL of the page viewed."),
        help_text=_("The full URL of the page the user visited.")
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_comment=_("Timestamp when the page view occurred."),
        help_text=_("The time when the user viewed the page.")
    )

    class Meta:
        db_table = "page_views"
        verbose_name = _("Page View")
        verbose_name_plural = _("Page Views")

    def __str__(self):
        return f"Page View {self.url} at {self.timestamp}"
