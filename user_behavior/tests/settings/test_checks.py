import sys
from unittest.mock import MagicMock, patch

import pytest

from user_behavior.settings.checks import check_user_behavior_settings
from user_behavior.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.settings,
    pytest.mark.settings_checks,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestUserBehaviorSettings:
    @patch("user_behavior.settings.checks.config")
    def test_valid_settings(self, mock_config: MagicMock) -> None:
        """
        Test that valid settings produce no errors.

        Args:
        ----
            mock_config (MagicMock): Mocked configuration object with valid settings.

        Asserts:
        -------
            No errors are returned when all settings are valid.
        """
        # Mock all config values to be valid
        # Admin settings
        mock_config.admin_has_add_permission = True
        mock_config.admin_has_change_permission = False
        mock_config.admin_has_delete_permission = True
        mock_config.admin_has_module_permission = False
        mock_config.admin_site_class = "django.contrib.admin.sites.AdminSite"

        # Global API settings
        mock_config.api_allow_list = True
        mock_config.api_allow_retrieve = False
        mock_config.api_allow_create = True
        mock_config.base_user_throttle_rate = "100/day"
        mock_config.staff_user_throttle_rate = "200/hour"

        mock_config.api_page_view_ordering_fields = ["timestamp", "url"]
        mock_config.api_page_view_search_fields = ["url"]
        mock_config.api_user_session_ordering_fields = ["start_time"]
        mock_config.api_user_session_search_fields = ["session_id"]
        mock_config.api_user_interaction_ordering_fields = ["timestamp", "event_type"]
        mock_config.api_user_interaction_search_fields = ["element"]

        mock_config.get_setting.side_effect = lambda name, default: default

        errors = check_user_behavior_settings(None)
        assert not errors, f"Expected no errors for valid settings, but got {errors}"

    @patch("user_behavior.settings.checks.config")
    def test_invalid_boolean_settings(self, mock_config: MagicMock) -> None:
        """
        Test that invalid boolean settings return errors.

        Args:
        ----
            mock_config (MagicMock): Mocked configuration object with invalid boolean settings.

        Asserts:
        -------
            Errors are returned for invalid boolean values in settings.
        """
        # Set valid defaults for non-boolean settings
        mock_config.api_page_view_ordering_fields = ["timestamp"]
        mock_config.api_page_view_search_fields = ["url"]
        mock_config.api_user_session_ordering_fields = ["start_time"]
        mock_config.api_user_session_search_fields = ["session_id"]
        mock_config.api_user_interaction_ordering_fields = ["timestamp"]
        mock_config.api_user_interaction_search_fields = ["element"]
        mock_config.base_user_throttle_rate = "100/day"
        mock_config.staff_user_throttle_rate = "200/hour"

        # Invalid boolean settings
        mock_config.admin_has_add_permission = "not_boolean"
        mock_config.admin_has_change_permission = "not_boolean"
        mock_config.admin_has_delete_permission = "not_boolean"
        mock_config.admin_has_module_permission = "not_boolean"
        mock_config.api_allow_list = "not_boolean"
        mock_config.api_allow_retrieve = "not_boolean"
        mock_config.api_allow_create = "not_boolean"

        mock_config.get_setting.side_effect = lambda name, default: default

        errors = check_user_behavior_settings(None)
        assert (
            len(errors) == 7
        ), f"Expected 7 errors for invalid booleans, but got {len(errors)}"
        error_ids = [error.id for error in errors]
        expected_ids = [
            f"user_behavior.E001_{mock_config.prefix}ADMIN_HAS_ADD_PERMISSION",
            f"user_behavior.E001_{mock_config.prefix}ADMIN_HAS_CHANGE_PERMISSION",
            f"user_behavior.E001_{mock_config.prefix}ADMIN_HAS_DELETE_PERMISSION",
            f"user_behavior.E001_{mock_config.prefix}ADMIN_HAS_MODULE_PERMISSION",
            f"user_behavior.E001_{mock_config.prefix}API_ALLOW_LIST",
            f"user_behavior.E001_{mock_config.prefix}API_ALLOW_RETRIEVE",
            f"user_behavior.E001_{mock_config.prefix}API_ALLOW_CREATE",
        ]
        assert all(
            eid in error_ids for eid in expected_ids
        ), f"Expected error IDs {expected_ids}, got {error_ids}"

    @patch("user_behavior.settings.checks.config")
    def test_invalid_list_settings(self, mock_config: MagicMock) -> None:
        """
        Test that invalid list settings return errors.

        Args:
        ----
            mock_config (MagicMock): Mocked configuration object with invalid list settings.

        Asserts:
        -------
            Errors are returned for invalid list values in settings.
        """
        # Valid boolean and throttle settings
        mock_config.admin_has_add_permission = True
        mock_config.admin_has_change_permission = False
        mock_config.admin_has_delete_permission = True
        mock_config.admin_has_module_permission = False
        mock_config.api_allow_list = True
        mock_config.api_allow_retrieve = False
        mock_config.api_allow_create = True
        mock_config.base_user_throttle_rate = "100/day"
        mock_config.staff_user_throttle_rate = "200/hour"

        # Invalid list settings
        mock_config.api_page_view_ordering_fields = []  # Empty list
        mock_config.api_page_view_search_fields = [123]  # Invalid type
        mock_config.api_user_session_ordering_fields = []  # Empty list
        mock_config.api_user_session_search_fields = [456]  # Invalid type
        mock_config.api_user_interaction_ordering_fields = []  # Empty list
        mock_config.api_user_interaction_search_fields = [789]  # Invalid type

        mock_config.get_setting.side_effect = lambda name, default: default

        errors = check_user_behavior_settings(None)
        assert (
            len(errors) == 6
        ), f"Expected 6 errors for invalid lists, but got {len(errors)}"
        error_ids = [error.id for error in errors]
        expected_ids = [
            f"user_behavior.E003_{mock_config.prefix}API_PAGE_VIEW_ORDERING_FIELDS",
            f"user_behavior.E004_{mock_config.prefix}API_PAGE_VIEW_SEARCH_FIELDS",
            f"user_behavior.E003_{mock_config.prefix}API_USER_SESSION_ORDERING_FIELDS",
            f"user_behavior.E004_{mock_config.prefix}API_USER_SESSION_SEARCH_FIELDS",
            f"user_behavior.E003_{mock_config.prefix}API_USER_INTERACTION_ORDERING_FIELDS",
            f"user_behavior.E004_{mock_config.prefix}API_USER_INTERACTION_SEARCH_FIELDS",
        ]
        assert all(
            eid in error_ids for eid in expected_ids
        ), f"Expected error IDs {expected_ids}, got {error_ids}"

    @patch("user_behavior.settings.checks.config")
    def test_invalid_throttle_rate(self, mock_config: MagicMock) -> None:
        """
        Test that invalid throttle rates return errors.

        Args:
        ----
            mock_config (MagicMock): Mocked configuration object with invalid throttle rates.

        Asserts:
        -------
            Errors are returned for invalid throttle rates.
        """
        # Valid boolean and list settings
        mock_config.admin_has_add_permission = True
        mock_config.admin_has_change_permission = False
        mock_config.admin_has_delete_permission = True
        mock_config.admin_has_module_permission = False
        mock_config.api_allow_list = True
        mock_config.api_allow_retrieve = False
        mock_config.api_allow_create = True
        mock_config.api_page_view_ordering_fields = ["timestamp"]
        mock_config.api_page_view_search_fields = ["url"]
        mock_config.api_user_session_ordering_fields = ["start_time"]
        mock_config.api_user_session_search_fields = ["session_id"]
        mock_config.api_user_interaction_ordering_fields = ["timestamp"]
        mock_config.api_user_interaction_search_fields = ["element"]

        # Invalid throttle rates
        mock_config.base_user_throttle_rate = "invalid_rate"
        mock_config.staff_user_throttle_rate = "abc/hour"

        mock_config.get_setting.side_effect = lambda name, default: default

        errors = check_user_behavior_settings(None)
        assert (
            len(errors) == 2
        ), f"Expected 2 errors for invalid throttle rates, but got {len(errors)}"
        error_ids = [error.id for error in errors]
        expected_ids = [
            f"user_behavior.E005_{mock_config.prefix}BASE_USER_THROTTLE_RATE",
            f"user_behavior.E007_{mock_config.prefix}STAFF_USER_THROTTLE_RATE",
        ]
        assert all(
            eid in error_ids for eid in expected_ids
        ), f"Expected error IDs {expected_ids}, got {error_ids}"

    @patch("user_behavior.settings.checks.config")
    def test_invalid_path_import(self, mock_config: MagicMock) -> None:
        """
        Test that invalid path import settings return errors.

        Args:
        ----
            mock_config (MagicMock): Mocked configuration object with invalid paths.

        Asserts:
        -------
            Errors are returned for invalid path imports.
        """
        # Valid boolean, list, and throttle settings
        mock_config.admin_has_add_permission = True
        mock_config.admin_has_change_permission = False
        mock_config.admin_has_delete_permission = True
        mock_config.admin_has_module_permission = False
        mock_config.api_allow_list = True
        mock_config.api_allow_retrieve = False
        mock_config.api_allow_create = True
        mock_config.base_user_throttle_rate = "100/day"
        mock_config.staff_user_throttle_rate = "200/hour"
        mock_config.api_page_view_ordering_fields = ["timestamp"]
        mock_config.api_page_view_search_fields = ["url"]
        mock_config.api_user_session_ordering_fields = ["start_time"]
        mock_config.api_user_session_search_fields = ["session_id"]
        mock_config.api_user_interaction_ordering_fields = ["timestamp"]
        mock_config.api_user_interaction_search_fields = ["element"]

        mock_config.get_setting.side_effect = (
            lambda name, default: "invalid.path.ClassName"
        )

        errors = check_user_behavior_settings(None)
        assert (
            len(errors) == 19
        ), f"Expected 19 errors for invalid paths, but got {len(errors)}"
        error_ids = [error.id for error in errors]
        expected_ids = [
            f"user_behavior.E010_{mock_config.prefix}ADMIN_SITE_CLASS",
            f"user_behavior.E010_{mock_config.prefix}API_PAGE_VIEW_SERIALIZER_CLASS",
            f"user_behavior.E011_{mock_config.prefix}API_PAGE_VIEW_THROTTLE_CLASSES",
            f"user_behavior.E010_{mock_config.prefix}API_PAGE_VIEW_PAGINATION_CLASS",
            f"user_behavior.E010_{mock_config.prefix}API_PAGE_VIEW_EXTRA_PERMISSION_CLASS",
            f"user_behavior.E011_{mock_config.prefix}API_PAGE_VIEW_PARSER_CLASSES",
            f"user_behavior.E010_{mock_config.prefix}API_PAGE_VIEW_FILTERSET_CLASS",
            f"user_behavior.E010_{mock_config.prefix}API_USER_SESSION_SERIALIZER_CLASS",
            f"user_behavior.E011_{mock_config.prefix}API_USER_SESSION_THROTTLE_CLASSES",
            f"user_behavior.E010_{mock_config.prefix}API_USER_SESSION_PAGINATION_CLASS",
            f"user_behavior.E010_{mock_config.prefix}API_USER_SESSION_EXTRA_PERMISSION_CLASS",
            f"user_behavior.E011_{mock_config.prefix}API_USER_SESSION_PARSER_CLASSES",
            f"user_behavior.E010_{mock_config.prefix}API_USER_SESSION_FILTERSET_CLASS",
            f"user_behavior.E010_{mock_config.prefix}API_USER_INTERACTION_SERIALIZER_CLASS",
            f"user_behavior.E011_{mock_config.prefix}API_USER_INTERACTION_THROTTLE_CLASSES",
            f"user_behavior.E010_{mock_config.prefix}API_USER_INTERACTION_PAGINATION_CLASS",
            f"user_behavior.E010_{mock_config.prefix}API_USER_INTERACTION_EXTRA_PERMISSION_CLASS",
            f"user_behavior.E011_{mock_config.prefix}API_USER_INTERACTION_PARSER_CLASSES",
            f"user_behavior.E010_{mock_config.prefix}API_USER_INTERACTION_FILTERSET_CLASS",
        ]
        assert all(
            eid in error_ids for eid in expected_ids
        ), f"Expected error IDs {expected_ids}, got {error_ids}"
