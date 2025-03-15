import sys
from unittest.mock import Mock

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from user_behavior.models import PageView, UserSession
from user_behavior.settings.conf import config
from user_behavior.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.api,
    pytest.mark.api_views,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestPageViewViewSet:
    """
    Tests for the PageViewViewSet API endpoints.

    This test class verifies the behavior of the PageViewViewSet,
    ensuring that the list, retrieve, and create methods function correctly
    under various configurations and user permissions.

    Tests:
    -------
    - test_list_page_views: Verifies that the list endpoint returns a 200 OK status and includes results when allowed.
    - test_retrieve_page_view: Checks that the retrieve endpoint returns a 200 OK status and the correct page view when allowed.
    - test_create_page_view: Tests that the create endpoint returns a 201 Created status when allowed.
    - test_list_page_views_disabled: Tests that the list endpoint returns a 405 Method Not Allowed status when disabled.
    - test_retrieve_page_views_disabled: Tests that the retrieve endpoint returns a 405 Method Not Allowed status when disabled.
    """

    def test_list_page_views(
        self,
        api_client: APIClient,
        admin_user: User,
        monkeypatch: Mock,
        page_view: PageView,
    ):
        """
        Test the list endpoint for PageView.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            monkeypatch (Mock): Mock object for patching during tests.
            page_view (PageView): A sample PageView instance to ensure data is present.

        Asserts:
        --------
            The response status code is 200.
            The response data contains a 'results' key with data.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_list = True  # Ensure the list method is allowed

        url = reverse("pageview-list")  # Adjust based on your URL configuration
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert "results" in response.data, "Expected 'results' in response data."
        assert len(response.data["results"]) > 0, "Expected data in the results."
        assert (
            response.data["results"][0]["url"] == page_view.url
        ), f"Expected URL {page_view.url}, got {response.data['results'][0]['url']}"

    def test_retrieve_page_view(
        self,
        api_client: APIClient,
        admin_user: User,
        page_view: PageView,
    ):
        """
        Test the retrieve endpoint for PageView.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            page_view (PageView): The PageView instance to retrieve.

        Asserts:
        --------
            The response status code is 200.
            The response data contains the correct PageView ID and URL.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_retrieve = True  # Ensure the retrieve method is allowed

        url = reverse("pageview-detail", kwargs={"pk": page_view.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."

        assert (
            response.data["id"] == page_view.pk
        ), f"Expected PageView ID {page_view.pk}, got {response.data['id']}."
        assert (
            response.data["url"] == page_view.url
        ), f"Expected URL {page_view.url}, got {response.data['url']}."

    def test_create_page_view(
        self,
        api_client: APIClient,
        admin_user: User,
        user_session: UserSession,
    ):
        """
        Test the create endpoint for PageView.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            user_session (UserSession): The UserSession instance to associate with the new PageView.

        Asserts:
        --------
            The response status code is 201.
            The response data contains the created PageView's URL.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_create = True  # Ensure the create method is allowed

        url = reverse("pageview-list")
        data = {
            "session_id": user_session.session_id,
            "url": "https://example.com/new-page",
        }
        response = api_client.post(url, data, format="json")

        assert (
            response.status_code == 201
        ), f"Expected 201 Created, got {response.status_code}."
        assert (
            response.data["url"] == "https://example.com/new-page"
        ), f"Expected URL 'https://example.com/new-page', got {response.data['url']}"
        assert PageView.objects.count() == 1, "Expected one PageView to be created"

    def test_create_page_view_with_invalid_session_id(
        self,
        api_client: APIClient,
        admin_user: User,
    ):
        """
        Test the create endpoint for PageView.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.

        Asserts:
        --------
            The response status code is 400 due to invalid session ID.
            The response data contains the session_id key as error key.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_create = True  # Ensure the create method is allowed

        url = reverse("pageview-list")
        data = {
            "session_id": "invalid",
            "url": "https://example.com/new-page",
        }
        response = api_client.post(url, data, format="json")

        assert (
            response.status_code == 400
        ), f"Expected 400 Bad Request, got {response.status_code}."
        assert response.data["session_id"] == [
            ErrorDetail(string="User with this session ID not found", code="invalid")
        ], f"Expected session ID error 'User with this session ID not found', got {response.data}"

    @pytest.mark.parametrize("is_staff", [True, False])
    def test_list_page_views_disabled(
        self, api_client: APIClient, admin_user: User, user: User, is_staff: bool
    ):
        """
        Test the list view when disabled via configuration.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            user (User): A regular user for testing permissions.
            is_staff (bool): Indicates whether to authenticate as an admin or regular user.

        Asserts:
        --------
            The response status code is 405.
        """
        _user = admin_user if is_staff else user
        api_client.force_authenticate(user=_user)

        config.api_allow_list = False  # Disable the list method

        url = reverse("pageview-list")
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."
