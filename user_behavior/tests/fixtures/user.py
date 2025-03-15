import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user(db) -> User:
    """
    Fixture to create a standard User instance for testing.

    Args:
        db: The database fixture to set up the test database.

    Returns:
        User: The created User instance with username "testuser".
    """
    return User.objects.create_user(
        username="testuser", password="12345", email="testuser@example.com"
    )


@pytest.fixture
def admin_user(db) -> User:
    """
    Fixture to create a superuser with admin access for testing.

    Args:
        db: The database fixture to set up the test database.

    Returns:
        User: The created superuser with username "admin".
    """
    return User.objects.create_superuser(username="admin", password="password")
