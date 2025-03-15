from django_filters import rest_framework as filters
from django.utils.translation import gettext_lazy as _
from user_behavior.models import PageView


class PageViewFilter(filters.FilterSet):
    """FilterSet for the PageView model API.

    Provides rich filtering capabilities for PageView instances, including filters
    for session, URL, and timestamp fields.
    """
    # Session-related filters
    session_id = filters.CharFilter(
        field_name="session__id",
        lookup_expr="exact",
        label=_("Session ID"),
        help_text=_("Filter by exact session ID."),
    )
    session_id_contains = filters.CharFilter(
        field_name="session__id",
        lookup_expr="icontains",
        label=_("Session ID Contains"),
        help_text=_(
            "Filter by session ID containing the specified value (case-insensitive)."
        ),
    )

    # URL-related filters
    url = filters.CharFilter(
        field_name="url",
        lookup_expr="exact",
        label=_("URL"),
        help_text=_("Filter by exact URL."),
    )
    url_contains = filters.CharFilter(
        field_name="url",
        lookup_expr="icontains",
        label=_("URL Contains"),
        help_text=_("Filter by URL containing the specified value (case-insensitive)."),
    )
    url_startswith = filters.CharFilter(
        field_name="url",
        lookup_expr="istartswith",
        label=_("URL Starts With"),
        help_text=_("Filter by URL starting with the specified value (case-insensitive)."),
    )
    url_endswith = filters.CharFilter(
        field_name="url",
        lookup_expr="iendswith",
        label=_("URL Ends With"),
        help_text=_("Filter by URL ending with the specified value (case-insensitive)."),
    )

    # Timestamp-related filters
    timestamp = filters.DateTimeFilter(
        field_name="timestamp",
        lookup_expr="exact",
        label=_("Timestamp"),
        help_text=_("Filter by exact timestamp."),
    )
    timestamp_after = filters.DateTimeFilter(
        field_name="timestamp",
        lookup_expr="gte",
        label=_("Timestamp After"),
        help_text=_("Filter for page views on or after the specified timestamp."),
    )
    timestamp_before = filters.DateTimeFilter(
        field_name="timestamp",
        lookup_expr="lte",
        label=_("Timestamp Before"),
        help_text=_("Filter for page views on or before the specified timestamp."),
    )
    timestamp_range = filters.DateTimeFromToRangeFilter(
        field_name="timestamp",
        label=_("Timestamp Range"),
        help_text=_("Filter for page views within a timestamp range."),
    )
    timestamp_date = filters.DateFilter(
        field_name="timestamp",
        lookup_expr="date",
        label=_("Timestamp Date"),
        help_text=_("Filter by the date portion of the timestamp."),
    )

    class Meta:
        model = PageView
        fields = ["session", "url", "timestamp"]
