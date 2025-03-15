from django.contrib import admin

from user_behavior.mixins.admin.permission import AdminPermissionControlMixin
from user_behavior.models import UserSession
from user_behavior.settings.conf import config


@admin.register(UserSession, site=config.admin_site_class)
class UserSessionAdmin(AdminPermissionControlMixin, admin.ModelAdmin):
    list_display = (
        "session_id",
        "user_agent",
        "ip_address",
        "start_time",
        "end_time",
        "user_id",
    )
    list_filter = ("start_time", "end_time", "user_id")
    search_fields = ("session_id", "user_agent", "ip_address", "user_id")
    readonly_fields = ("start_time",)
    fieldsets = (
        (None, {"fields": ("session_id", "user_agent", "ip_address", "user_id")}),
        (
            "Timestamps",
            {"fields": ("start_time", "end_time"), "classes": ("collapse",)},
        ),
    )
