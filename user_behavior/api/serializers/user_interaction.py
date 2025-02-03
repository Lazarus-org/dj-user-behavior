from rest_framework import serializers
from user_behavior.models import UserSession, PageView, UserInteraction


class UserInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = "__all__"
        read_only_fields = ("timestamp",)