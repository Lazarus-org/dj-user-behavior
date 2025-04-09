from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('user_behavior/', include("user_behavior.urls")),
]
