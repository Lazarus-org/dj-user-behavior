from rest_framework import serializers
from user_behavior.models import UserSession, PageView, UserInteraction

from .user_session import UserSessionSerializer


class PageViewSerializer(serializers.ModelSerializer):
    session_id = serializers.CharField(write_only=True)
    session = UserSessionSerializer(read_only=True)
    class Meta:
        model = PageView
        fields = ["url", "timestamp", "session_id", "session"]
        read_only_fields = ("timestamp",)


    def validate_session_id(self, value):
        session = value
        is_session_exits = UserSession.objects.filter(session_id=session).first()
        if not is_session_exits:
            raise serializers.ValidationError(
                    "User with this session ID not found"
            )
        return is_session_exits
    

    def create(self, validated_data):
        session = validated_data.get("session_id")
        url = validated_data.get("url")

        page_view = PageView()
        page_view.url = url
        page_view.session = session
        page_view.save()

        return page_view
    



        