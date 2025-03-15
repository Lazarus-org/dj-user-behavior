from rest_framework import serializers

from user_behavior.models import UserSession


class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = "__all__"
        read_only_fields = ("start_time",)
