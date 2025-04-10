import json
from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Count, DurationField, ExpressionWrapper, F
from django.db.models.functions import TruncDay
from django.utils import timezone
from django.views.generic import TemplateView

from user_behavior.settings.conf import config

from .models import PageView, UserInteraction, UserSession
from .utils.user_agent import detect_browser


class UserBehaviorReportView(TemplateView):
    """A class-based view to display user behavior analytics for the last 7
    days.

    This view renders interaction, page view, session duration, and
    browser usage data in a template, with permission checks applied.

    """

    template_name = "report.html"
    permission_classes = [config.report_view_permission_class]

    def get_permissions(self):
        """Instantiate and return the list of permissions that this view
        requires."""
        return [permission() for permission in self.permission_classes if permission]

    def check_permissions(self, request):
        """Check if the request should be permitted, raising PermissionDenied
        if not."""
        for permission in self.get_permissions():
            if not hasattr(
                permission, "has_permission"
            ) or not permission.has_permission(request, self):
                raise PermissionDenied()

    def dispatch(self, request, *args, **kwargs):
        """Handle request dispatch with permission checks."""
        self.check_permissions(request)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Generate context data for the report template."""
        context = super().get_context_data(**kwargs)

        # Define the date range: last 7 days including today
        end_date = timezone.now()
        start_date = end_date - timedelta(days=6)

        # Query UserInteraction: Event Type Counts (total over last 7 days)
        interactions = (
            UserInteraction.objects.filter(
                timestamp__gte=start_date, timestamp__lte=end_date
            )
            .values("event_type")
            .annotate(count=Count("id"))
            .order_by("event_type")
        )
        interaction_data = [
            {
                "interaction": item["event_type"],
                "count": item["count"],
            }
            for item in interactions
        ]

        # Query UserInteraction: Timestamps (daily counts)
        timestamps = (
            UserInteraction.objects.filter(
                timestamp__gte=start_date, timestamp__lte=end_date
            )
            .annotate(day=TruncDay("timestamp"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("-day")
        )
        timestamps_data = [
            {
                "day": item["day"].strftime("%A"),
                "count": item["count"],
                "timestamp": item["day"].isoformat(),
            }
            for item in timestamps
        ]

        # Query PageView: Daily counts with URL breakdown
        page_views = (
            PageView.objects.filter(timestamp__gte=start_date, timestamp__lte=end_date)
            .annotate(day=TruncDay("timestamp"))
            .values("day")
            .annotate(total_count=Count("id"))
            .order_by("-day")
        )
        url_details = (
            PageView.objects.filter(timestamp__gte=start_date, timestamp__lte=end_date)
            .annotate(day=TruncDay("timestamp"))
            .values("day", "url")
            .annotate(url_count=Count("id"))
            .order_by("-day", "url")
        )
        start_times_data = []
        for day_data in page_views:
            day = day_data["day"]
            total_count = day_data["total_count"]
            urls_in_day = [
                {"url": item["url"], "count": item["url_count"]}
                for item in url_details
                if item["day"] == day
            ]
            start_times_data.append(
                {
                    "day": day.strftime("%A"),
                    "count": total_count,
                    "timestamp": day.isoformat(),
                    "urls": urls_in_day,
                }
            )

        # Query UserSession: Session Duration and Count (by day)
        sessions = (
            UserSession.objects.filter(
                start_time__gte=start_date,
                start_time__lte=end_date,
                end_time__isnull=False,
            )
            .annotate(day=TruncDay("start_time"))
            .annotate(
                duration=ExpressionWrapper(
                    F("end_time") - F("start_time"), output_field=DurationField()
                )
            )
        )
        daily_counts = (
            sessions.values("day").annotate(count=Count("id")).order_by("-day")
        )
        daily_durations = (
            sessions.values("day")
            .annotate(avg_duration=Avg("duration"))
            .order_by("-day")
        )
        start_end_times_data = []
        for count_item, duration_item in zip(daily_counts, daily_durations):
            if count_item["day"] == duration_item["day"]:
                avg_duration_minutes = (
                    int(duration_item["avg_duration"].total_seconds() / 60)
                    if duration_item["avg_duration"]
                    and duration_item["avg_duration"].total_seconds() > 0
                    else 0
                )
                start_end_times_data.append(
                    {
                        "day": count_item["day"].strftime("%A"),
                        "duration": f"{avg_duration_minutes}",
                        "count": count_item["count"],
                        "timestamp": count_item["day"].isoformat(),
                    }
                )

        # Query UserSession: Browser Usage Percentage (last 7 days)
        browser_sessions = (
            UserSession.objects.filter(
                start_time__gte=start_date, start_time__lte=end_date
            )
            .values("user_agent")
            .annotate(count=Count("id"))
        )
        total_sessions = sum(item["count"] for item in browser_sessions)
        browser_counts = {}
        for session in browser_sessions:
            browser = detect_browser(session["user_agent"])[0]
            browser_counts[browser] = browser_counts.get(browser, 0) + session["count"]
        browser_data = [
            {
                "browser": browser,
                "count": count,
                "percentage": (
                    round((count / total_sessions) * 100, 2)
                    if total_sessions > 0
                    else 0
                ),
            }
            for browser, count in browser_counts.items()
        ]
        browser_data.sort(key=lambda x: x["count"], reverse=True)

        # Populate context
        context.update(
            {
                "admin_name": (
                    str(self.request.user)
                    if self.request.user.is_authenticated
                    else "Admin"
                ),
                "interaction_data": json.dumps(interaction_data),
                "timestamps_data": json.dumps(timestamps_data),
                "page_views": json.dumps(start_times_data),
                "start_end_times_data": json.dumps(start_end_times_data),
                "browser_data": json.dumps(browser_data),
            }
        )
        return context
