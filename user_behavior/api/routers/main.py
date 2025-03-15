from rest_framework.routers import DefaultRouter

from user_behavior.api.views import (
    PageViewViewSet,
    UserInteractionViewSet,
    UserSessionViewSet,
)

router = DefaultRouter()
router.register(r"sessions", UserSessionViewSet)
router.register(r"pageviews", PageViewViewSet)
router.register(r"interactions", UserInteractionViewSet)

urlpatterns = router.urls
