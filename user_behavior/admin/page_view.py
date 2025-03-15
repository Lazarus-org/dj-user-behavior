from django.contrib import admin

from user_behavior.mixins.admin.permission import AdminPermissionControlMixin
from user_behavior.models import PageView
from user_behavior.settings.conf import config


@admin.register(PageView, site=config.admin_site_class)
class PageViewAdmin(AdminPermissionControlMixin, admin.ModelAdmin):
    list_display = ("session", "url", "timestamp")
    autocomplete_fields = ("session",)
    list_filter = ("timestamp",)
    search_fields = ("url", "session__session_id")
    readonly_fields = ("timestamp",)
    fieldsets = (
        (None, {"fields": ("session", "url")}),
        ("Timestamp", {"fields": ("timestamp",), "classes": ("collapse",)}),
    )
