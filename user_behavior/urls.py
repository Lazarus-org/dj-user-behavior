from django.urls import path
from rest_framework.routers import DefaultRouter

from user_behavior.api.views import (
    PageViewViewSet,
    UserInteractionViewSet,
    UserSessionViewSet,
)
from user_behavior.views import UserBehaviorReportView

router = DefaultRouter()
router.register(r"sessions", UserSessionViewSet)
router.register(r"pageviews", PageViewViewSet)
router.register(r"interactions", UserInteractionViewSet)

urlpatterns = router.urls
urlpatterns += [
    path("report/", UserBehaviorReportView.as_view(), name="user_behavior_report"),
]
