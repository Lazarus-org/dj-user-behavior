from rest_framework import serializers
from user_behavior.models import UserSession, PageView, UserInteraction

from .user_session import UserSessionSerializer

class UserInteractionSerializer(serializers.ModelSerializer):
    session_id = serializers.CharField(write_only=True)
    session = UserSessionSerializer(read_only=True)
    class Meta:
        model = UserInteraction
        fields = ["session_id", "session", "event_type", "element", "metadata"]
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
        event_type = validated_data.get("event_type")
        element = validated_data.get("element")
        metadata = validated_data.get("metadata") if validated_data.get("metadata") else {}
        breakpoint()

        user_interaction = UserInteraction()
        user_interaction.session = session
        user_interaction.event_type = event_type
        user_interaction.element = element
        user_interaction.metadata = metadata
        user_interaction.save()

        return user_interaction
