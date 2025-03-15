from django.contrib import admin

from user_behavior.mixins.admin.permission import AdminPermissionControlMixin
from user_behavior.models import UserInteraction
from user_behavior.settings.conf import config


@admin.register(UserInteraction, site=config.admin_site_class)
class UserInteractionAdmin(AdminPermissionControlMixin, admin.ModelAdmin):
    list_display = ("session", "event_type", "element", "timestamp")
    autocomplete_fields = ("session",)
    list_filter = ("event_type", "timestamp")
    search_fields = ("element", "session__session_id")
    readonly_fields = ("timestamp",)
    fieldsets = (
        (None, {"fields": ("session", "event_type", "element")}),
        ("Metadata", {"fields": ("metadata",), "classes": ("collapse",)}),
        ("Timestamp", {"fields": ("timestamp",), "classes": ("collapse",)}),
    )
