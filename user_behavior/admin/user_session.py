# tracker/admin.py
from django.contrib import admin
from user_behavior.models import UserSession, PageView, UserInteraction

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ("session_id", "user_agent", "ip_address", "start_time", "end_time", "user_id")
    list_filter = ("start_time", "end_time", "user_id")
    search_fields = ("session_id", "user_agent", "ip_address", "user_id")
    readonly_fields = ("start_time",)
    fieldsets = (
        (None, {
            "fields": ("session_id", "user_agent", "ip_address", "user_id")
        }),
        ("Timestamps", {
            "fields": ("start_time", "end_time"),
            "classes": ("collapse",)
        }),
    )

