# tracker/admin.py
from django.contrib import admin
from user_behavior.models import UserSession, PageView, UserInteraction

@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ("session", "event_type", "element", "timestamp")
    autocomplete_fields = ("session",)
    list_filter = ("event_type", "timestamp")
    search_fields = ("element", "session__session_id")
    readonly_fields = ("timestamp",)
    fieldsets = (
        (None, {
            "fields": ("session", "event_type", "element")
        }),
        ("Metadata", {
            "fields": ("metadata",),
            "classes": ("collapse",)
        }),
        ("Timestamp", {
            "fields": ("timestamp",),
            "classes": ("collapse",)
        }),
    )