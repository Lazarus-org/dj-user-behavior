from typing import Any, List

from django.conf import settings
from django.utils.module_loading import import_string

from user_behavior.constants.default_settings import (
    admin_settings,
    api_page_view_settings,
    api_settings,
    api_user_interaction_settings,
    api_user_session_settings,
    throttle_settings,
    view_settings,
)
from user_behavior.constants.types import DefaultPath, OptionalPaths


# pylint: disable=too-many-instance-attributes
class UserBehaviorConfig:
    """A configuration handler.

    allowing dynamic settings loading from the Django settings, with
    default fallbacks.

    """

    prefix = "USER_BEHAVIOR_"

    def __init__(self) -> None:
        # Admin settings
        self.admin_has_add_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_ADD_PERMISSION",
            admin_settings.admin_has_add_permission,
        )
        self.admin_has_change_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_CHANGE_PERMISSION",
            admin_settings.admin_has_change_permission,
        )
        self.admin_has_delete_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_DELETE_PERMISSION",
            admin_settings.admin_has_delete_permission,
        )
        self.admin_has_module_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_MODULE_PERMISSION",
            admin_settings.admin_has_module_permission,
        )
        # Admin site class
        self.admin_site_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}ADMIN_SITE_CLASS",
            admin_settings.admin_site_class,
        )

        # Global API settings
        self.api_allow_list: bool = self.get_setting(
            f"{self.prefix}API_ALLOW_LIST", api_settings.allow_list
        )
        self.api_allow_retrieve: bool = self.get_setting(
            f"{self.prefix}API_ALLOW_RETRIEVE", api_settings.allow_retrieve
        )
        self.api_allow_create: bool = self.get_setting(
            f"{self.prefix}API_ALLOW_CREATE", api_settings.allow_create
        )
        self.base_user_throttle_rate: str = self.get_setting(
            f"{self.prefix}BASE_USER_THROTTLE_RATE",
            throttle_settings.base_user_throttle_rate,
        )
        self.staff_user_throttle_rate: str = self.get_setting(
            f"{self.prefix}STAFF_USER_THROTTLE_RATE",
            throttle_settings.staff_user_throttle_rate,
        )

        # PageView-specific API settings
        self.api_page_view_serializer_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_PAGE_VIEW_SERIALIZER_CLASS",
            api_page_view_settings.page_view_serializer,
        )
        self.api_page_view_ordering_fields: List[str] = self.get_setting(
            f"{self.prefix}API_PAGE_VIEW_ORDERING_FIELDS",
            api_page_view_settings.ordering_fields,
        )
        self.api_page_view_search_fields: List[str] = self.get_setting(
            f"{self.prefix}API_PAGE_VIEW_SEARCH_FIELDS",
            api_page_view_settings.search_fields,
        )
        self.api_page_view_throttle_classes: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_PAGE_VIEW_THROTTLE_CLASSES",
            throttle_settings.throttle_class,  # Default to global throttle
        )
        self.api_page_view_pagination_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_PAGE_VIEW_PAGINATION_CLASS",
            api_settings.pagination_class,
        )
        self.api_page_view_extra_permission_class: OptionalPaths = (
            self.get_optional_paths(
                f"{self.prefix}API_PAGE_VIEW_EXTRA_PERMISSION_CLASS",
                api_settings.extra_permission_class,
            )
        )
        self.api_page_view_parser_classes: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_PAGE_VIEW_PARSER_CLASSES",
            api_settings.parser_classes,
        )
        self.api_page_view_filterset_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_PAGE_VIEW_FILTERSET_CLASS",
            api_page_view_settings.filterset_class,
        )

        # UserSession-specific API settings
        self.api_user_session_serializer_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_USER_SESSION_SERIALIZER_CLASS",
            api_user_session_settings.user_session_serializer,
        )
        self.api_user_session_ordering_fields: List[str] = self.get_setting(
            f"{self.prefix}API_USER_SESSION_ORDERING_FIELDS",
            api_user_session_settings.ordering_fields,
        )
        self.api_user_session_search_fields: List[str] = self.get_setting(
            f"{self.prefix}API_USER_SESSION_SEARCH_FIELDS",
            api_user_session_settings.search_fields,
        )
        self.api_user_session_throttle_classes: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_USER_SESSION_THROTTLE_CLASSES",
            throttle_settings.throttle_class,
        )
        self.api_user_session_pagination_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_USER_SESSION_PAGINATION_CLASS",
            api_settings.pagination_class,
        )
        self.api_user_session_extra_permission_class: OptionalPaths = (
            self.get_optional_paths(
                f"{self.prefix}API_USER_SESSION_EXTRA_PERMISSION_CLASS",
                api_settings.extra_permission_class,
            )
        )
        self.api_user_session_parser_classes: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_USER_SESSION_PARSER_CLASSES",
            api_settings.parser_classes,
        )
        self.api_user_session_filterset_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_USER_SESSION_FILTERSET_CLASS",
            api_user_session_settings.filterset_class,
        )

        # UserInteraction-specific API settings
        self.api_user_interaction_serializer_class: OptionalPaths = (
            self.get_optional_paths(
                f"{self.prefix}API_USER_INTERACTION_SERIALIZER_CLASS",
                api_user_interaction_settings.user_interaction_serializer,
            )
        )
        self.api_user_interaction_ordering_fields: List[str] = self.get_setting(
            f"{self.prefix}API_USER_INTERACTION_ORDERING_FIELDS",
            api_user_interaction_settings.ordering_fields,
        )
        self.api_user_interaction_search_fields: List[str] = self.get_setting(
            f"{self.prefix}API_USER_INTERACTION_SEARCH_FIELDS",
            api_user_interaction_settings.search_fields,
        )
        self.api_user_interaction_throttle_classes: OptionalPaths = (
            self.get_optional_paths(
                f"{self.prefix}API_USER_INTERACTION_THROTTLE_CLASSES",
                throttle_settings.throttle_class,
            )
        )
        self.api_user_interaction_pagination_class: OptionalPaths = (
            self.get_optional_paths(
                f"{self.prefix}API_USER_INTERACTION_PAGINATION_CLASS",
                api_settings.pagination_class,
            )
        )
        self.api_user_interaction_extra_permission_class: OptionalPaths = (
            self.get_optional_paths(
                f"{self.prefix}API_USER_INTERACTION_EXTRA_PERMISSION_CLASS",
                api_settings.extra_permission_class,
            )
        )
        self.api_user_interaction_parser_classes: OptionalPaths = (
            self.get_optional_paths(
                f"{self.prefix}API_USER_INTERACTION_PARSER_CLASSES",
                api_settings.parser_classes,
            )
        )
        self.api_user_interaction_filterset_class: OptionalPaths = (
            self.get_optional_paths(
                f"{self.prefix}API_USER_INTERACTION_FILTERSET_CLASS",
                api_user_interaction_settings.filterset_class,
            )
        )

        # Report View settings
        self.report_view_permission_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}REPORT_VIEW_PERMISSION_CLASS",
            view_settings.report_permission_class,
        )

    def get_setting(self, setting_name: str, default_value: Any) -> Any:
        """Retrieve a setting from Django settings with a default fallback.

        Args:
            setting_name (str): The name of the setting to retrieve.
            default_value (Any): The default value to return if the setting is not found.

        Returns:
            Any: The value of the setting or the default value if not found.

        """
        return getattr(settings, setting_name, default_value)

    def get_optional_paths(
        self,
        setting_name: str,
        default_path: DefaultPath,
    ) -> OptionalPaths:
        """Dynamically load a method or class path on a setting, or return None
        if the setting is None or invalid.

        Args:
            setting_name (str): The name of the setting for the method or class path.
            default_path (Optional[Union[str, List[str]]): The default import path for the method or class.

        Returns:
            Optional[Union[Type[Any], List[Type[Any]]]]: The imported method or class or None
             if import fails or the path is invalid.

        """
        _path: DefaultPath = self.get_setting(setting_name, default_path)

        if _path and isinstance(_path, str):
            try:
                return import_string(_path)
            except ImportError:
                return None
        elif _path and isinstance(_path, list):
            try:
                return [import_string(path) for path in _path if isinstance(path, str)]
            except ImportError:
                return []

        return None


# Create a global config object
config: UserBehaviorConfig = UserBehaviorConfig()
