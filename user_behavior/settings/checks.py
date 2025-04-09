from typing import Any, List

from django.core.checks import Error, register

from user_behavior.settings.conf import config
from user_behavior.validators.config_validators import (
    validate_boolean_setting,
    validate_list_fields,
    validate_optional_path_setting,
    validate_optional_paths_setting,
    validate_throttle_rate,
)


@register()
def check_user_behavior_settings(app_configs: Any, **kwargs: Any) -> List[Error]:
    """Check and validate user behavior settings in the Django configuration.

    This function performs validation of various user behavior-related settings
    defined in the Django settings. It returns a list of errors if any issues are found.

    Parameters:
    -----------
    app_configs : Any
        Passed by Django during checks (not used here).

    kwargs : Any
        Additional keyword arguments for flexibility.

    Returns:
    --------
    List[Error]
        A list of `Error` objects for any detected configuration issues.

    """
    errors: List[Error] = []

    # Validate Admin settings
    errors.extend(
        validate_boolean_setting(
            config.admin_has_add_permission, f"{config.prefix}ADMIN_HAS_ADD_PERMISSION"
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.admin_has_change_permission,
            f"{config.prefix}ADMIN_HAS_CHANGE_PERMISSION",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.admin_has_delete_permission,
            f"{config.prefix}ADMIN_HAS_DELETE_PERMISSION",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.admin_has_module_permission,
            f"{config.prefix}ADMIN_HAS_MODULE_PERMISSION",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}ADMIN_SITE_CLASS", None),
            f"{config.prefix}ADMIN_SITE_CLASS",
        )
    )

    # Validate Global API settings
    errors.extend(
        validate_boolean_setting(
            config.api_allow_list, f"{config.prefix}API_ALLOW_LIST"
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_allow_retrieve, f"{config.prefix}API_ALLOW_RETRIEVE"
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_allow_create, f"{config.prefix}API_ALLOW_CREATE"
        )
    )
    errors.extend(
        validate_throttle_rate(
            config.base_user_throttle_rate, f"{config.prefix}BASE_USER_THROTTLE_RATE"
        )
    )
    errors.extend(
        validate_throttle_rate(
            config.staff_user_throttle_rate, f"{config.prefix}STAFF_USER_THROTTLE_RATE"
        )
    )

    # Validate PageView-specific API settings
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_PAGE_VIEW_SERIALIZER_CLASS", None),
            f"{config.prefix}API_PAGE_VIEW_SERIALIZER_CLASS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_page_view_ordering_fields,
            f"{config.prefix}API_PAGE_VIEW_ORDERING_FIELDS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_page_view_search_fields,
            f"{config.prefix}API_PAGE_VIEW_SEARCH_FIELDS",
        )
    )
    errors.extend(
        validate_optional_paths_setting(
            config.get_setting(f"{config.prefix}API_PAGE_VIEW_THROTTLE_CLASSES", None),
            f"{config.prefix}API_PAGE_VIEW_THROTTLE_CLASSES",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_PAGE_VIEW_PAGINATION_CLASS", None),
            f"{config.prefix}API_PAGE_VIEW_PAGINATION_CLASS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_PAGE_VIEW_EXTRA_PERMISSION_CLASS", None
            ),
            f"{config.prefix}API_PAGE_VIEW_EXTRA_PERMISSION_CLASS",
        )
    )
    errors.extend(
        validate_optional_paths_setting(
            config.get_setting(f"{config.prefix}API_PAGE_VIEW_PARSER_CLASSES", None),
            f"{config.prefix}API_PAGE_VIEW_PARSER_CLASSES",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_PAGE_VIEW_FILTERSET_CLASS", None),
            f"{config.prefix}API_PAGE_VIEW_FILTERSET_CLASS",
        )
    )

    # Validate UserSession-specific API settings
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_USER_SESSION_SERIALIZER_CLASS", None
            ),
            f"{config.prefix}API_USER_SESSION_SERIALIZER_CLASS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_user_session_ordering_fields,
            f"{config.prefix}API_USER_SESSION_ORDERING_FIELDS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_user_session_search_fields,
            f"{config.prefix}API_USER_SESSION_SEARCH_FIELDS",
        )
    )
    errors.extend(
        validate_optional_paths_setting(
            config.get_setting(
                f"{config.prefix}API_USER_SESSION_THROTTLE_CLASSES", None
            ),
            f"{config.prefix}API_USER_SESSION_THROTTLE_CLASSES",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_USER_SESSION_PAGINATION_CLASS", None
            ),
            f"{config.prefix}API_USER_SESSION_PAGINATION_CLASS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_USER_SESSION_EXTRA_PERMISSION_CLASS", None
            ),
            f"{config.prefix}API_USER_SESSION_EXTRA_PERMISSION_CLASS",
        )
    )
    errors.extend(
        validate_optional_paths_setting(
            config.get_setting(f"{config.prefix}API_USER_SESSION_PARSER_CLASSES", None),
            f"{config.prefix}API_USER_SESSION_PARSER_CLASSES",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_USER_SESSION_FILTERSET_CLASS", None
            ),
            f"{config.prefix}API_USER_SESSION_FILTERSET_CLASS",
        )
    )

    # Validate UserInteraction-specific API settings
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_USER_INTERACTION_SERIALIZER_CLASS", None
            ),
            f"{config.prefix}API_USER_INTERACTION_SERIALIZER_CLASS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_user_interaction_ordering_fields,
            f"{config.prefix}API_USER_INTERACTION_ORDERING_FIELDS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_user_interaction_search_fields,
            f"{config.prefix}API_USER_INTERACTION_SEARCH_FIELDS",
        )
    )
    errors.extend(
        validate_optional_paths_setting(
            config.get_setting(
                f"{config.prefix}API_USER_INTERACTION_THROTTLE_CLASSES", None
            ),
            f"{config.prefix}API_USER_INTERACTION_THROTTLE_CLASSES",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_USER_INTERACTION_PAGINATION_CLASS", None
            ),
            f"{config.prefix}API_USER_INTERACTION_PAGINATION_CLASS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_USER_INTERACTION_EXTRA_PERMISSION_CLASS", None
            ),
            f"{config.prefix}API_USER_INTERACTION_EXTRA_PERMISSION_CLASS",
        )
    )
    errors.extend(
        validate_optional_paths_setting(
            config.get_setting(
                f"{config.prefix}API_USER_INTERACTION_PARSER_CLASSES", None
            ),
            f"{config.prefix}API_USER_INTERACTION_PARSER_CLASSES",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_USER_INTERACTION_FILTERSET_CLASS", None
            ),
            f"{config.prefix}API_USER_INTERACTION_FILTERSET_CLASS",
        )
    )

    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}REPORT_VIEW_PERMISSION_CLASS", None),
            f"{config.prefix}REPORT_VIEW_PERMISSION_CLASS",
        )
    )

    return errors
