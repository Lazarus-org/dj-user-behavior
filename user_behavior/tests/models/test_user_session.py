import sys

import pytest

from user_behavior.models import UserSession
from user_behavior.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestUserSessionModel:
    """
    Test suite for the UserSession model.
    """

    def test_str_method(self, user_session: UserSession) -> None:
        """
        Test that the __str__ method returns the correct string representation of a user session.

        Asserts:
        -------
            - The string representation includes the session ID and user ID.
        """
        expected_str = (
            f"Session {user_session.session_id} - User ID: ({user_session.user_id})"
        )
        assert (
            str(user_session) == expected_str
        ), f"Expected the __str__ method to return '{expected_str}', but got '{str(user_session)}'."
