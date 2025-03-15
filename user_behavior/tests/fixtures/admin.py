from unittest.mock import Mock

import pytest
from django.contrib.admin import AdminSite
from django.http import HttpRequest
from django.test import RequestFactory

from user_behavior.admin import PageViewAdmin
from user_behavior.models import PageView


@pytest.fixture
def request_factory() -> RequestFactory:
    """
    Fixture to provide an instance of RequestFactory.

    Returns:
    -------
        RequestFactory: An instance of Django's RequestFactory.
    """
    return RequestFactory()


@pytest.fixture
def mock_request():
    """Fixture to provide a mock HttpRequest object.

    Returns:
    -------
        Mock: A Mock instance of Django's HttpRequest.
    """
    return Mock(spec=HttpRequest)


@pytest.fixture
def admin_site() -> AdminSite:
    """
    Fixture to provide an instance of AdminSite.

    Returns:
    -------
        AdminSite: An instance of Django's AdminSite.
    """
    return AdminSite()


@pytest.fixture
def page_view_admin(admin_site: AdminSite) -> PageViewAdmin:
    """
    Fixture to provide an instance of PageViewAdmin.

    Args:
    ----
        admin_site (AdminSite): An instance of Django's AdminSite.

    Returns:
    -------
        PageViewAdmin: An instance of PageViewAdmin.
    """
    return PageViewAdmin(PageView, admin_site)
