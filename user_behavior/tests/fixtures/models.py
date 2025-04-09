import pytest
from django.utils import timezone
from user_behavior.models import UserSession, PageView, UserInteraction
from user_behavior.models.helper.enum.event_type import EventType


@pytest.fixture
def user_session() -> UserSession:
    """
    Fixture to create a UserSession instance.
    """
    return UserSession.objects.create(
        session_id="test_session_123",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        ip_address="192.168.1.1",
        start_time=timezone.now(),
        end_time=None,  # Ongoing session
        user_id="user123",
    )


@pytest.fixture
def another_user_session() -> UserSession:
    """
    Fixture to create a UserSession instance.
    """
    return UserSession.objects.create(
        session_id="test_session_1234",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        ip_address="192.168.1.1",
        start_time=timezone.now(),
        end_time=timezone.now(),
        user_id="user123",
    )


@pytest.fixture
def page_view(user_session: UserSession) -> PageView:
    """
    Fixture to create a PageView instance linked to a UserSession.

    Args:
        user_session: The UserSession fixture to associate with this PageView.
    """
    return PageView.objects.create(
        session=user_session,
        url="https://example.com/test-page",
        timestamp=timezone.now(),
    )


@pytest.fixture
def user_interaction(user_session: UserSession) -> UserInteraction:
    """
    Fixture to create a UserInteraction instance linked to a UserSession.

    Args:
        user_session: The UserSession fixture to associate with this UserInteraction.
    """
    return UserInteraction.objects.create(
        session=user_session,
        event_type=EventType.CLICK,
        element="#submit-button",
        timestamp=timezone.now(),
        metadata={"x_coord": 100, "y_coord": 200},
    )
