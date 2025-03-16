from rest_framework import mixins

from user_behavior.api.serializers.helper.get_serializer_cls import (
    page_view_serializer_class,
)
from user_behavior.api.views.base import BaseViewSet
from user_behavior.models import PageView


class PageViewViewSet(
    BaseViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    config_prefix = "page_view"
    queryset = PageView.objects.select_related("session").all()
    serializer_class = page_view_serializer_class()
