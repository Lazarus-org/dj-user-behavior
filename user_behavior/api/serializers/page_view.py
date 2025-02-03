from rest_framework import serializers
from user_behavior.models import UserSession, PageView, UserInteraction

class PageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageView
        fields = "__all__"
        read_only_fields = ("timestamp",)

