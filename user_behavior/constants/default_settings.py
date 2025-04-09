from dataclasses import dataclass, field
from typing import List, Optional

# pylint: disable=too-many-instance-attributes


@dataclass(frozen=True)
class DefaultAdminSettings:
    admin_site_class: Optional[str] = None
    admin_has_add_permission: bool = True
    admin_has_change_permission: bool = True
    admin_has_delete_permission: bool = True
    admin_has_module_permission: bool = True


@dataclass(frozen=True)
class DefaultThrottleSettings:
    base_user_throttle_rate: str = "30/minute"
    staff_user_throttle_rate: str = "100/minute"
    throttle_class: str = "user_behavior.api.throttlings.RoleBasedUserRateThrottle"


@dataclass(frozen=True)
class DefaultPageViewAPISettings:
    filterset_class: Optional[str] = None
    ordering_fields: List[str] = field(default_factory=lambda: ["timestamp"])
    search_fields: List[str] = field(
        default_factory=lambda: ["url", "session__session_id"]
    )
    page_view_serializer = None


@dataclass(frozen=True)
class DefaultUserSessionAPISettings:
    filterset_class: Optional[str] = None
    ordering_fields: List[str] = field(
        default_factory=lambda: [
            "start_time",
            "end_time",
        ]
    )
    search_fields: List[str] = field(
        default_factory=lambda: ["session_id", "user_agent", "ip_address"]
    )
    user_session_serializer = None


@dataclass(frozen=True)
class DefaultUserInteractionAPISettings:
    filterset_class: Optional[str] = None
    ordering_fields: List[str] = field(default_factory=lambda: ["timestamp"])
    search_fields: List[str] = field(
        default_factory=lambda: ["session__session_id", "element"]
    )
    user_interaction_serializer = None


@dataclass(frozen=True)
class DefaultAPISettings:
    allow_list: bool = True
    allow_retrieve: bool = True
    allow_create: bool = True
    extra_permission_class: Optional[str] = None
    pagination_class: str = "user_behavior.api.paginations.DefaultLimitOffSetPagination"
    parser_classes: List[str] = field(
        default_factory=lambda: [
            "rest_framework.parsers.JSONParser",
            "rest_framework.parsers.MultiPartParser",
            "rest_framework.parsers.FormParser",
        ]
    )


@dataclass(frozen=True)
class DefaultViewSettings:
    report_permission_class: Optional[str] = "rest_framework.permissions.IsAdminUser"


admin_settings = DefaultAdminSettings()
throttle_settings = DefaultThrottleSettings()
api_settings = DefaultAPISettings()
api_page_view_settings = DefaultPageViewAPISettings()
api_user_session_settings = DefaultUserSessionAPISettings()
api_user_interaction_settings = DefaultUserInteractionAPISettings()
view_settings = DefaultViewSettings()
