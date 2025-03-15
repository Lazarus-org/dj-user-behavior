from io import StringIO

import logging
import pytest


@pytest.fixture
def log_capture():
    """Fixture to capture log output."""
    buffer = StringIO()
    handler = logging.StreamHandler(buffer)
    logger = logging.getLogger("user_behavior")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    yield buffer
    logger.removeHandler(handler)
