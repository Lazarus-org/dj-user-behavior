# tracker/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user_behavior.api.views.api import UserSessionViewSet, PageViewViewSet, UserInteractionViewSet

router = DefaultRouter()
router.register(r"sessions", UserSessionViewSet)
router.register(r"pageviews", PageViewViewSet)
router.register(r"interactions", UserInteractionViewSet)

urlpatterns = router.urls
