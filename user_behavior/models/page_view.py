from django.db import models
from django.utils.translation import gettext_lazy as _


class PageView(models.Model):
    session = models.ForeignKey(
        to="UserSession",
        on_delete=models.CASCADE,
        verbose_name=_("Session"),
        db_comment="The session associated with this page view.",
        help_text=_("The session during which this page view occurred."),
    )
    url = models.URLField(
        verbose_name=_("Page URL"),
        db_comment="The URL of the page viewed.",
        help_text=_("The full URL of the page the user visited."),
    )
    timestamp = models.DateTimeField(
        verbose_name=_("Timestamp"),
        auto_now_add=True,
        db_comment="Timestamp when the page view occurred.",
        help_text=_("The time when the user viewed the page."),
    )

    class Meta:
        verbose_name = _("Page View")
        verbose_name_plural = _("Page Views")

    def __str__(self):
        return f"Page View {self.url} at {self.timestamp}"
