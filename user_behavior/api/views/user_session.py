from rest_framework import mixins

from user_behavior.api.serializers.helper.get_serializer_cls import (
    user_session_serializer_class,
)
from user_behavior.api.views.base import BaseViewSet
from user_behavior.models import UserSession


class UserSessionViewSet(
    BaseViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    config_prefix = "user_session"
    queryset = UserSession.objects.all()
    serializer_class = user_session_serializer_class()
