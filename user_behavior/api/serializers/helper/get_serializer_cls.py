from typing import Type

from rest_framework.serializers import BaseSerializer

from user_behavior.settings.conf import config


def page_view_serializer_class() -> Type[BaseSerializer]:
    """Get the serializer class for the PageView model, either from config or
    the default.

    Returns:
        The configured serializer class from settings or the default PageViewSerializer.

    """
    from user_behavior.api.serializers.page_view import PageViewSerializer

    return config.api_page_view_serializer_class or PageViewSerializer


def user_session_serializer_class() -> Type[BaseSerializer]:
    """Get the serializer class for the UserSession model, either from config
    or the default.

    Returns:
        The configured serializer class from settings or the default UserSessionSerializer.

    """
    from user_behavior.api.serializers.user_session import UserSessionSerializer

    return config.api_user_session_serializer_class or UserSessionSerializer


def user_interaction_serializer_class() -> Type[BaseSerializer]:
    """Get the serializer class for the UserInteraction model, either from
    config or the default.

    Returns:
        The configured serializer class from settings or the default UserInteractionSerializer.

    """
    from user_behavior.api.serializers.user_interaction import UserInteractionSerializer

    return config.api_user_interaction_serializer_class or UserInteractionSerializer
