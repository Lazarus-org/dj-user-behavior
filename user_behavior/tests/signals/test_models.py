import sys

import pytest
from user_behavior.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.signals,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestUserBehaviorSignals:
    """
    Test class for User Behavior signal handlers.

    Tests the log_create_update and log_delete signal handlers for UserSession,
    PageView, and UserInteraction models, ensuring they log correctly on create,
    update, and delete actions.
    """

    @pytest.mark.django_db
    def test_log_update_usersession(self, user_session, log_capture):
        """
        Test that updating a UserSession logs the correct message.
        """
        log_capture.truncate(0)  # Clear previous logs
        user_session.user_agent = "Updated Agent"
        user_session.save()
        log_output = log_capture.getvalue()
        expected_message = f"UserSession updated: {user_session}"
        assert (
            expected_message in log_output
        ), f"Expected log message '{expected_message}', got '{log_output}'"

    @pytest.mark.django_db
    def test_log_delete_usersession(self, user_session, log_capture):
        """
        Test that deleting a UserSession logs the correct message.
        """
        log_capture.truncate(0)  # Clear previous logs
        user_session_str = str(user_session)  # Capture string before deletion
        user_session.delete()
        log_output = log_capture.getvalue()
        expected_message = f"UserSession deleted: {user_session_str}"
        assert (
            expected_message in log_output
        ), f"Expected log message '{expected_message}', got '{log_output}'"

    @pytest.mark.django_db
    def test_log_update_pageview(self, page_view, log_capture):
        """
        Test that updating a PageView logs the correct message.
        """
        log_capture.truncate(0)  # Clear previous logs
        page_view.url = "https://example.com/updated-page"
        page_view.save()
        log_output = log_capture.getvalue()
        expected_message = f"PageView updated: {page_view}"
        assert (
            expected_message in log_output
        ), f"Expected log message '{expected_message}', got '{log_output}'"

    @pytest.mark.django_db
    def test_log_delete_pageview(self, page_view, log_capture):
        """
        Test that deleting a PageView logs the correct message.
        """
        log_capture.truncate(0)  # Clear previous logs
        page_view_str = str(page_view)  # Capture string before deletion
        page_view.delete()
        log_output = log_capture.getvalue()
        expected_message = f"PageView deleted: {page_view_str}"
        assert (
            expected_message in log_output
        ), f"Expected log message '{expected_message}', got '{log_output}'"

    @pytest.mark.django_db
    def test_log_update_userinteraction(self, user_interaction, log_capture):
        """
        Test that updating a UserInteraction logs the correct message.
        """
        log_capture.truncate(0)  # Clear previous logs
        user_interaction.element = "#updated-button"
        user_interaction.save()
        log_output = log_capture.getvalue()
        expected_message = f"UserInteraction updated: {user_interaction}"
        assert (
            expected_message in log_output
        ), f"Expected log message '{expected_message}', got '{log_output}'"

    @pytest.mark.django_db
    def test_log_delete_userinteraction(self, user_interaction, log_capture):
        """
        Test that deleting a UserInteraction logs the correct message.
        """
        log_capture.truncate(0)  # Clear previous logs
        user_interaction_str = str(user_interaction)  # Capture string before deletion
        user_interaction.delete()
        log_output = log_capture.getvalue()
        expected_message = f"UserInteraction deleted: {user_interaction_str}"
        assert (
            expected_message in log_output
        ), f"Expected log message '{expected_message}', got '{log_output}'"
