import pytest
import json
import sys
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from user_behavior.views import UserBehaviorReportView
from user_behavior.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.views,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestUserBehaviorReportView:
    """
    Tests for the UserBehaviorReportView using pytest.

    This test class verifies the behavior of the UserBehaviorReportView, ensuring that:
    - Authenticated users with appropriate permissions can access the view.
    - Unauthenticated users are denied access.
    - Additional permissions (e.g., from APIKEY_AUTH_VIEW_PERMISSION_CLASS) are enforced.
    - The correct template is rendered with user behavior data.
    """

    def test_authenticated_user_access(
        self, request_factory, admin_user, report_url, page_view, another_user_session
    ):
        """
        Test that an authenticated user with permissions can access the UserBehaviorReportView.
        """

        request = request_factory.get(report_url)
        request.user = admin_user

        view = UserBehaviorReportView.as_view()
        response = view(request)

        assert (
            response.status_code == 200
        ), "Authenticated user should get a 200 OK response."
        assert (
            "report.html" in response.template_name
        ), "Should render report.html template."
        assert (
            "interaction_data" in response.context_data
        ), "Context should include interaction data."
        assert (
            "timestamps_data" in response.context_data
        ), "Context should include timestamps data."
        assert (
            "page_views" in response.context_data
        ), "Context should include page views data."
        assert (
            "start_end_times_data" in response.context_data
        ), "Context should include session data."
        assert (
            "browser_data" in response.context_data
        ), "Context should include browser data."

    def test_unauthenticated_user_access(self, request_factory, report_url):
        """
        Test that an unauthenticated user is denied access to the UserBehaviorReportView.
        """
        request = request_factory.get(report_url)
        request.user = AnonymousUser()  # Simulate an unauthenticated user

        view = UserBehaviorReportView.as_view()

        with pytest.raises(PermissionDenied):
            view(request)

    def test_permission_denied_for_non_admin(self, request_factory, user, report_url):
        """
        Test that a non-admin user without required permissions is denied access.
        Assumes default permission is IsAdminUser.
        """
        # Setup: Create a regular user without admin privileges
        request = request_factory.get(report_url)
        request.user = user  # Regular user, not admin

        view = UserBehaviorReportView.as_view()

        with pytest.raises(PermissionDenied):
            view(request)

    def test_context_data_empty(self, request_factory, admin_user, report_url):
        """
        Test that the view renders correctly with empty data.
        """
        request = request_factory.get(report_url)
        request.user = admin_user

        view = UserBehaviorReportView.as_view()
        response = view(request)

        assert response.status_code == 200, "Should return 200 OK even with no data."
        interaction_data = json.loads(response.context_data["interaction_data"])
        timestamps_data = json.loads(response.context_data["timestamps_data"])
        page_views = json.loads(response.context_data["page_views"])
        start_end_times_data = json.loads(response.context_data["start_end_times_data"])
        browser_data = json.loads(response.context_data["browser_data"])

        assert isinstance(interaction_data, list), "interaction_data should be a list."
        assert isinstance(timestamps_data, list), "timestamps_data should be a list."
        assert isinstance(page_views, list), "page_views should be a list."
        assert isinstance(
            start_end_times_data, list
        ), "start_end_times_data should be a list."
        assert isinstance(browser_data, list), "browser_data should be a list."
        assert len(interaction_data) == 0, "Should be empty with no interactions."
        assert len(timestamps_data) == 0, "Should be empty with no timestamps."
        assert len(page_views) == 0, "Should be empty with no page views."
        assert len(start_end_times_data) == 0, "Should be empty with no sessions."
        assert len(browser_data) == 0, "Should be empty with no browser data."
