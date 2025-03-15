import sys

import pytest

from user_behavior.models import UserInteraction
from user_behavior.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestUserInteractionModel:
    """
    Test suite for the UserInteraction model.
    """

    def test_str_method(self, user_interaction: UserInteraction) -> None:
        """
        Test that the __str__ method returns the correct string representation of a user interaction.

        Asserts:
        -------
            - The string representation includes the expected str.
        """
        expected_str = f"{user_interaction.event_type} on {user_interaction.element} at {user_interaction.timestamp}"
        assert (
            str(user_interaction) == expected_str
        ), f"Expected the __str__ method to return '{expected_str}', but got '{str(user_interaction)}'."
