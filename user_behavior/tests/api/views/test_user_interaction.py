import sys
from unittest.mock import Mock

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.permissions import AllowAny
from rest_framework.test import APIClient
from rest_framework.throttling import UserRateThrottle

from user_behavior.models import UserInteraction, UserSession
from user_behavior.settings.conf import config
from user_behavior.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON
from user_behavior.models.helper.enum.event_type import EventType

pytestmark = [
    pytest.mark.api,
    pytest.mark.api_views,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestUserInteractionViewSet:
    """
    Tests for the UserInteractionViewSet API endpoints.

    This test class verifies the behavior of the UserInteractionViewSet,
    ensuring that the list, retrieve, and create methods function correctly
    under various configurations and user permissions.

    Tests:
    -------
    - test_list_user_interactions: Verifies that the list endpoint returns a 200 OK status and includes results when allowed.
    - test_retrieve_user_interaction: Checks that the retrieve endpoint returns a 200 OK status and the correct interaction when allowed.
    - test_create_user_interaction: Tests that the create endpoint returns a 201 Created status when allowed.
    - test_list_user_interactions_disabled: Tests that the list endpoint returns a 405 Method Not Allowed status when disabled.
    - test_retrieve_user_interactions_disabled: Tests that the retrieve endpoint returns a 405 Method Not Allowed status when disabled.
    """

    def test_list_user_interactions(
        self,
        api_client: APIClient,
        admin_user: User,
        monkeypatch: Mock,
        user_interaction: UserInteraction,
    ):
        """
        Test the list endpoint for UserInteraction.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            monkeypatch (Mock): Mock object for patching during tests.
            user_interaction (UserInteraction): A sample UserInteraction instance to ensure data is present.

        Asserts:
        --------
            The response status code is 200.
            The response data contains a 'results' key with data.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_list = True  # Ensure the list method is allowed

        url = reverse("userinteraction-list")
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert "results" in response.data, "Expected 'results' in response data."
        assert len(response.data["results"]) > 0, "Expected data in the results."
        assert (
            response.data["results"][0]["event_type"] == user_interaction.event_type
        ), f"Expected event_type {user_interaction.event_type}, got {response.data['results'][0]['event_type']}"
        assert (
            response.data["results"][0]["element"] == user_interaction.element
        ), f"Expected element {user_interaction.element}, got {response.data['results'][0]['element']}"

    def test_retrieve_user_interaction(
        self,
        api_client: APIClient,
        admin_user: User,
        user_interaction: UserInteraction,
    ):
        """
        Test the retrieve endpoint for UserInteraction.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            user_interaction (UserInteraction): The UserInteraction instance to retrieve.

        Asserts:
        --------
            The response status code is 200.
            The response data contains the correct UserInteraction ID, event_type, and element.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_retrieve = True  # Ensure the retrieve method is allowed

        url = reverse("userinteraction-detail", kwargs={"pk": user_interaction.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            response.data["id"] == user_interaction.pk
        ), f"Expected UserInteraction ID {user_interaction.pk}, got {response.data['id']}."
        assert (
            response.data["event_type"] == user_interaction.event_type
        ), f"Expected event_type {user_interaction.event_type}, got {response.data['event_type']}."
        assert (
            response.data["element"] == user_interaction.element
        ), f"Expected element {user_interaction.element}, got {response.data['element']}."

    def test_create_user_interaction(
        self,
        api_client: APIClient,
        admin_user: User,
        user_session: UserSession,
    ):
        """
        Test the create endpoint for UserInteraction.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            user_session (UserSession): The UserSession instance to associate with the new UserInteraction.

        Asserts:
        --------
            The response status code is 201.
            The response data contains the created UserInteraction's event_type and element.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_create = True  # Ensure the create method is allowed

        url = reverse("userinteraction-list")
        data = {
            "session_id": user_session.session_id,
            "event_type": EventType.CLICK,
            "element": "#new-button",
            "metadata": {"x_coord": 150, "y_coord": 250},
        }
        response = api_client.post(url, data, format="json")

        assert (
            response.status_code == 201
        ), f"Expected 201 Created, got {response.status_code}. Response data: {response.data}"
        assert (
            response.data["event_type"] == EventType.CLICK
        ), f"Expected event_type {EventType.CLICK}, got {response.data['event_type']}"
        assert (
            response.data["element"] == "#new-button"
        ), f"Expected element '#new-button', got {response.data['element']}"
        assert (
            UserInteraction.objects.count() == 1
        ), "Expected one UserInteraction to be created"
        created_interaction = UserInteraction.objects.first()
        assert (
            created_interaction.session == user_session
        ), f"Expected session {user_session}, got {created_interaction.session}"

    def test_create_user_interaction_with_invalid_session_id(
        self,
        api_client: APIClient,
        admin_user: User,
    ):
        """
        Test the create endpoint for UserInteraction.

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

        url = reverse("userinteraction-list")
        data = {
            "session_id": "invalid",
            "event_type": EventType.CLICK,
            "element": "#new-button",
            "metadata": {"x_coord": 150, "y_coord": 250},
        }
        response = api_client.post(url, data, format="json")

        assert (
            response.status_code == 400
        ), f"Expected 400 Bad Request, got {response.status_code}."
        assert response.data["session_id"] == [
            ErrorDetail(string="User with this session ID not found", code="invalid")
        ], f"Expected session ID error 'User with this session ID not found', got {response.data}"

    @pytest.mark.parametrize("is_staff", [True, False])
    def test_list_user_interactions_disabled(
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

        url = reverse("userinteraction-list")
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_retrieve_user_interactions_disabled(
        self,
        api_client: APIClient,
        admin_user: User,
        user: User,
        user_interaction: UserInteraction,
    ):
        """
        Test the retrieve view when disabled via configuration.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            user (User): A regular user for testing permissions.
            user_interaction (UserInteraction): The UserInteraction instance to retrieve.

        Asserts:
        --------
            The response status code is 405.
        """
        for _user in [admin_user, user]:
            api_client.force_authenticate(user=_user)

            config.api_allow_retrieve = False  # Disable the retrieve method
            config.api_user_interaction_extra_permission_class = (
                AllowAny  # Test this config
            )

            url = reverse("userinteraction-detail", kwargs={"pk": user_interaction.pk})
            response = api_client.get(url)

            assert (
                response.status_code == 405
            ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_list_user_interactions_with_metadata_filter(
        self,
        api_client: APIClient,
        admin_user: User,
        user_interaction: UserInteraction,
    ):
        """
        Test the list endpoint with metadata filtering using filter_metadata method.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            user_interaction (UserInteraction): A sample UserInteraction instance with metadata.

        Asserts:
        --------
            The response status code is 200.
            The response data filters correctly based on metadata key-value pairs.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_list = True  # Ensure the list method is allowed

        # Test filtering by x_coord=100
        url = reverse("userinteraction-list")
        response = api_client.get(url, {"metadata": "x_coord=100"})
        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert "results" in response.data, "Expected 'results' in response data."
        assert (
            len(response.data["results"]) == 1
        ), f"Expected 1 result with x_coord=100, got {len(response.data['results'])}"
        assert (
            response.data["results"][0]["id"] == user_interaction.pk
        ), f"Expected ID {user_interaction.pk}, got {response.data['results'][0]['id']}"

        # Test filtering by y_coord=200
        response = api_client.get(url, {"metadata": "y_coord=200"})
        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            len(response.data["results"]) == 1
        ), f"Expected 1 result with y_coord=200, got {len(response.data['results'])}"

        # Test filtering with non-matching value
        response = api_client.get(url, {"metadata": "x_coord=²"})
        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            len(response.data["results"]) == 0
        ), f"Expected 0 results with x_coord=², got {len(response.data['results'])}"

        # Test invalid metadata format (no '=')
        response = api_client.get(url, {"metadata": "x_coord"})
        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            len(response.data["results"]) == 1
        ), f"Expected all results when metadata format is invalid, got {len(response.data['results'])}"

    def test_throttle_classes_configuration(
        self,
        api_client: APIClient,
        admin_user: User,
        user_interaction: UserInteraction,
    ):
        """
        Test throttle classes configuration inherited from BaseViewSet.

        Args:
        ----
            mock_config (Mock): Mocked config object to set throttle settings.
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            user_interaction (UserInteraction): A sample UserInteraction instance.

        Asserts:
        --------
            The throttle_classes are correctly set based on config settings.
            Invalid throttle settings raise a ValueError.
        """
        from user_behavior.api.views import UserInteractionViewSet

        api_client.force_authenticate(user=admin_user)

        # Test with specific throttle class
        config.api_allow_list = True
        config.api_user_interaction_throttle_classes = [UserRateThrottle]
        viewset = UserInteractionViewSet()
        viewset.request = api_client.get(reverse("userinteraction-list")).wsgi_request
        assert viewset.throttle_classes == [
            UserRateThrottle
        ], f"Expected [UserRateThrottle], got {viewset.throttle_classes}"

        # Test with list of throttle classes
        config.api_user_interaction_throttle_classes = [
            UserRateThrottle,
            AllowAny,
        ]  # AllowAny is not a throttle class
        viewset = UserInteractionViewSet()
        viewset.request = api_client.get(reverse("userinteraction-list")).wsgi_request
        assert viewset.throttle_classes == [
            UserRateThrottle
        ], f"Expected [UserRateThrottle], got {viewset.throttle_classes}"  # Only valid throttle classes included

        # Test with None (falls back to default which is None)
        config.api_user_interaction_throttle_classes = None
        viewset = UserInteractionViewSet()
        viewset.request = api_client.get(reverse("userinteraction-list")).wsgi_request
        assert (
            viewset.throttle_classes == []
        ), f"Expected empty list from default, got {viewset.throttle_classes}"

        # Test with invalid throttle setting
        config.api_user_interaction_throttle_classes = AllowAny
        with pytest.raises(ValueError) as exc_info:
            viewset = UserInteractionViewSet()
            viewset.request = api_client.get(
                reverse("userinteraction-list")
            ).wsgi_request
            viewset.throttle_classes  # Trigger initialization
        assert "Invalid throttle setting" in str(
            exc_info.value
        ), "Expected ValueError for invalid throttle setting"
