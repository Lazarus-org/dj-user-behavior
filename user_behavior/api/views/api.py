# tracker/views.py
from rest_framework import viewsets, mixins
from user_behavior.models import UserSession, PageView, UserInteraction
from user_behavior.api.serializers import UserSessionSerializer, PageViewSerializer, UserInteractionSerializer

class UserSessionViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer

class PageViewViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = PageView.objects.select_related("session").all()
    serializer_class = PageViewSerializer

class UserInteractionViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = UserInteraction.objects.select_related("session").all()
    serializer_class = UserInteractionSerializer