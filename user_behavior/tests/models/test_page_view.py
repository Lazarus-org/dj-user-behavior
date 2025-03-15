import sys

import pytest

from user_behavior.models import PageView
from user_behavior.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestPageViewModel:
    """
    Test suite for the PageView model.
    """

    def test_str_method(self, page_view: PageView) -> None:
        """
        Test that the __str__ method returns the correct string representation of a page view.

        Asserts:
        -------
            - The string representation includes the URL and timestamp.
        """
        expected_str = f"Page View {page_view.url} at {page_view.timestamp}"
        assert (
            str(page_view) == expected_str
        ), f"Expected the __str__ method to return '{expected_str}', but got '{str(page_view)}'."
