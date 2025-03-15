import sys
from unittest.mock import Mock

import pytest
from django.contrib import admin
from django.http import HttpRequest

from user_behavior.admin import PageViewAdmin
from user_behavior.models import PageView
from user_behavior.settings.conf import config
from user_behavior.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.admin,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestPageViewAdmin:
    """
    Tests for the PageViewAdmin class in the Django admin interface.

    This test class verifies the general functionality of the PageViewAdmin,
    ensuring it is properly configured and behaves as expected in the Django admin
    interface without relying on specific field names.

    Tests:
    -------
    - test_admin_registered: Verifies the PageView model is registered with PageViewAdmin.
    """

    def test_admin_registered(self):
        """
        Test that the Product model is registered with ProductAdmin in the admin site.

        Asserts:
        --------
            The admin site has Product registered with an instance of ProductAdmin.
        """
        assert isinstance(admin.site._registry[PageView], PageViewAdmin)

    def test_list_display_configured(self, page_view_admin: PageViewAdmin) -> None:
        """
        Test that the list_display attribute is defined and non-empty.

        This ensures the admin list view has some fields configured without
        specifying exact field names.

        Args:
        ----
            page_view_admin (PageViewAdmin): The admin class instance being tested.

        Asserts:
        --------
            list_display is a tuple or list and has at least one item.
        """
        assert isinstance(page_view_admin.list_display, (tuple, list))
        assert len(page_view_admin.list_display) > 0

    def test_admin_permissions(
        self, page_view_admin: PageViewAdmin, mock_request: HttpRequest
    ):
        """
        Test that admin permissions reflects the config setting.
        """
        # Test with permission denied
        config.admin_has_add_permission = False
        config.admin_has_change_permission = False
        config.admin_has_delete_permission = False
        config.admin_has_module_permission = False
        assert page_view_admin.has_add_permission(mock_request) is False
        assert page_view_admin.has_change_permission(mock_request) is False
        assert page_view_admin.has_delete_permission(mock_request) is False
        assert page_view_admin.has_module_permission(mock_request) is False

        # Test with permission granted
        config.admin_has_add_permission = True
        config.admin_has_change_permission = True
        config.admin_has_delete_permission = True
        config.admin_has_module_permission = True
        assert page_view_admin.has_add_permission(mock_request) is True
        assert page_view_admin.has_change_permission(mock_request) is True
        assert page_view_admin.has_delete_permission(mock_request) is True
        assert page_view_admin.has_module_permission(mock_request) is True
