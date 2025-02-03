# tracker/admin.py
from django.contrib import admin
from user_behavior.models import UserSession, PageView, UserInteraction

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ("session", "url", "timestamp")
    autocomplete_fields = ("session",)
    list_filter = ("timestamp",)
    search_fields = ("url", "session__session_id")
    readonly_fields = ("timestamp",)
    fieldsets = (
        (None, {
            "fields": ("session", "url")
        }),
        ("Timestamp", {
            "fields": ("timestamp",),
            "classes": ("collapse",)
        }),
    )

