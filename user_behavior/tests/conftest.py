import pytest
from user_behavior.tests.setup import configure_django_settings
from user_behavior.tests.fixtures import (
    page_view_admin,
    user_interaction,
    user_session,
    page_view,
    user,
    admin_user,
    admin_site,
    request_factory,
    mock_request,
    api_client,
    log_capture,
    report_url,
    another_user_session,
)
