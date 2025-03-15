import sys
from unittest.mock import patch

import pytest

from user_behavior.settings.conf import UserBehaviorConfig
from user_behavior.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.settings,
    pytest.mark.settings_conf,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestUserBehaviorConfig:
    """
    Test the exception handling in TestUserBehaviorConfig for optional class imports.
    """

    def test_import_error_handling(self) -> None:
        """
        Test that `get_optional_paths` handles ImportError and returns None when an invalid path is provided.

        Args:
        ----
            None

        Asserts:
        -------
            The result of `get_optional_paths` should be None when ImportError is raised.
        """
        config = UserBehaviorConfig()

        with patch(
            "django.utils.module_loading.import_string", side_effect=ImportError
        ):
            result = config.get_optional_paths(
                "INVALID_SETTING", "invalid.path.ClassName"
            )
            assert result is None

    def test_invalid_class_path_handling(self) -> None:
        """
        Test that `get_optional_classes` returns None when an invalid path is given (non-string).

        Args:
        ----
            None

        Asserts:
        -------
            The result of `get_optional_paths` should be None when a non-string path is provided.
        """
        config = UserBehaviorConfig()
        result = config.get_optional_paths("INVALID_SETTING", None)
        assert result is None

        result = config.get_optional_paths("INVALID_SETTING", ["INVALID_PATH"])
        assert not result
