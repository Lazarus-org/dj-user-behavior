from django_filters import rest_framework as filters
from django.utils.translation import gettext_lazy as _
from user_behavior.models import UserInteraction, UserSession
from user_behavior.models.helper.enum.event_type import EventType


class UserInteractionFilter(filters.FilterSet):
    """FilterSet for the UserInteraction model API.

    Provides rich filtering capabilities for UserInteraction instances, including filters
    for session, event type, element, timestamp, and metadata.
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

    # Event Type filters
    event_type = filters.ChoiceFilter(
        choices=EventType.choices,
        field_name="event_type",
        label=_("Event Type"),
        help_text=_("Filter by exact event type (e.g., click, scroll)."),
    )
    event_type_in = filters.MultipleChoiceFilter(
        choices=EventType.choices,
        field_name="event_type",
        label=_("Event Type In"),
        help_text=_("Filter by multiple event types (e.g., ['click', 'scroll'])."),
    )

    # Element filters
    element = filters.CharFilter(
        field_name="element",
        lookup_expr="exact",
        label=_("Element"),
        help_text=_("Filter by exact element (e.g., ID, class, or tag)."),
    )
    element_contains = filters.CharFilter(
        field_name="element",
        lookup_expr="icontains",
        label=_("Element Contains"),
        help_text=_(
            "Filter by element containing the specified value (case-insensitive)."
        ),
    )
    element_startswith = filters.CharFilter(
        field_name="element",
        lookup_expr="istartswith",
        label=_("Element Starts With"),
        help_text=_(
            "Filter by element starting with the specified value (case-insensitive)."
        ),
    )

    # Timestamp filters
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
        help_text=_("Filter for interactions on or after the specified timestamp."),
    )
    timestamp_before = filters.DateTimeFilter(
        field_name="timestamp",
        lookup_expr="lte",
        label=_("Timestamp Before"),
        help_text=_("Filter for interactions on or before the specified timestamp."),
    )
    timestamp_range = filters.DateTimeFromToRangeFilter(
        field_name="timestamp",
        label=_("Timestamp Range"),
        help_text=_("Filter for interactions within a timestamp range."),
    )
    timestamp_date = filters.DateFilter(
        field_name="timestamp",
        lookup_expr="date",
        label=_("Timestamp Date"),
        help_text=_("Filter by the date portion of the timestamp."),
    )

    # Metadata filters
    metadata = filters.CharFilter(
        method="filter_metadata",
        label=_("Metadata"),
        help_text=_("Filter by metadata key-value pairs (e.g., 'x_coord=100')."),
    )

    def filter_metadata(self, queryset, name, value):
        """Custom filter for metadata JSONField.

        Allows filtering by key-value pairs in the metadata field.
        Example: 'x_coord=100' filters for interactions where metadata['x_coord'] = 100.
        """
        if "=" not in value:
            return queryset
        key, val = value.split("=", 1)
        try:
            # Attempt to convert value to int or float if possible
            val = (
                int(val)
                if val.isdigit()
                else float(val) if val.replace(".", "").isdigit() else val
            )
        except ValueError:
            pass  # Keep as string if conversion fails
        return queryset.filter(**{f"metadata__{key}": val})

    class Meta:
        model = UserInteraction
        fields = ["session", "event_type", "element", "timestamp", "metadata"]
