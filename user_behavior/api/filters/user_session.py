from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from user_behavior.models import UserSession


class UserSessionFilter(filters.FilterSet):
    """FilterSet for the UserSession model API.

    Provides rich filtering capabilities for UserSession instances,
    including filters for session ID, user agent, IP address, start/end
    times, and user ID.

    """

    # Session ID filters
    session_id = filters.CharFilter(
        field_name="session_id",
        lookup_expr="exact",
        label=_("Session ID"),
        help_text=_("Filter by exact session ID."),
    )
    session_id_contains = filters.CharFilter(
        field_name="session_id",
        lookup_expr="icontains",
        label=_("Session ID Contains"),
        help_text=_(
            "Filter by session ID containing the specified value (case-insensitive)."
        ),
    )

    # User Agent filters
    user_agent = filters.CharFilter(
        field_name="user_agent",
        lookup_expr="exact",
        label=_("User Agent"),
        help_text=_("Filter by exact user agent string."),
    )
    user_agent_contains = filters.CharFilter(
        field_name="user_agent",
        lookup_expr="icontains",
        label=_("User Agent Contains"),
        help_text=_(
            "Filter by user agent containing the specified value (case-insensitive)."
        ),
    )

    # IP Address filters
    ip_address = filters.CharFilter(
        field_name="ip_address",
        lookup_expr="exact",
        label=_("IP Address"),
        help_text=_("Filter by exact IP address."),
    )
    ip_address_startswith = filters.CharFilter(
        field_name="ip_address",
        lookup_expr="startswith",
        label=_("IP Address Starts With"),
        help_text=_("Filter by IP address starting with the specified value."),
    )

    # Start Time filters
    start_time = filters.DateTimeFilter(
        field_name="start_time",
        lookup_expr="exact",
        label=_("Start Time"),
        help_text=_("Filter by exact start time."),
    )
    start_time_after = filters.DateTimeFilter(
        field_name="start_time",
        lookup_expr="gte",
        label=_("Start Time After"),
        help_text=_("Filter for sessions started on or after the specified time."),
    )
    start_time_before = filters.DateTimeFilter(
        field_name="start_time",
        lookup_expr="lte",
        label=_("Start Time Before"),
        help_text=_("Filter for sessions started on or before the specified time."),
    )
    start_time_range = filters.DateTimeFromToRangeFilter(
        field_name="start_time",
        label=_("Start Time Range"),
        help_text=_("Filter for sessions started within a time range."),
    )
    start_time_date = filters.DateFilter(
        field_name="start_time",
        lookup_expr="date",
        label=_("Start Time Date"),
        help_text=_("Filter by the date portion of the start time."),
    )

    # End Time filters
    end_time = filters.DateTimeFilter(
        field_name="end_time",
        lookup_expr="exact",
        label=_("End Time"),
        help_text=_("Filter by exact end time."),
    )
    end_time_after = filters.DateTimeFilter(
        field_name="end_time",
        lookup_expr="gte",
        label=_("End Time After"),
        help_text=_("Filter for sessions ended on or after the specified time."),
    )
    end_time_before = filters.DateTimeFilter(
        field_name="end_time",
        lookup_expr="lte",
        label=_("End Time Before"),
        help_text=_("Filter for sessions ended on or before the specified time."),
    )
    end_time_range = filters.DateTimeFromToRangeFilter(
        field_name="end_time",
        label=_("End Time Range"),
        help_text=_("Filter for sessions ended within a time range."),
    )
    end_time_date = filters.DateFilter(
        field_name="end_time",
        lookup_expr="date",
        label=_("End Time Date"),
        help_text=_("Filter by the date portion of the end time."),
    )
    end_time_isnull = filters.BooleanFilter(
        field_name="end_time",
        lookup_expr="isnull",
        label=_("End Time Is Null"),
        help_text=_(
            "Filter for sessions with no end time (ongoing sessions) if True, or ended sessions if False."
        ),
    )

    # User ID filters
    user_id = filters.CharFilter(
        field_name="user_id",
        lookup_expr="exact",
        label=_("User ID"),
        help_text=_("Filter by exact user ID."),
    )
    user_id_contains = filters.CharFilter(
        field_name="user_id",
        lookup_expr="icontains",
        label=_("User ID Contains"),
        help_text=_(
            "Filter by user ID containing the specified value (case-insensitive)."
        ),
    )
    user_id_isnull = filters.BooleanFilter(
        field_name="user_id",
        lookup_expr="isnull",
        label=_("User ID Is Null"),
        help_text=_(
            "Filter for sessions with no user ID (anonymous) if True, or with user ID if False."
        ),
    )

    class Meta:
        model = UserSession
        fields = [
            "session_id",
            "user_agent",
            "ip_address",
            "start_time",
            "end_time",
            "user_id",
        ]
