from rest_framework import mixins

from user_behavior.api.serializers.helper.get_serializer_cls import (
    user_interaction_serializer_class,
)
from user_behavior.api.views.base import BaseViewSet
from user_behavior.models import UserInteraction


class UserInteractionViewSet(
    BaseViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    config_prefix = "user_interaction"
    queryset = UserInteraction.objects.select_related("session").all()
    serializer_class = user_interaction_serializer_class()
