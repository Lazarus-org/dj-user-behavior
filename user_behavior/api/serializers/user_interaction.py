from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from user_behavior.api.serializers.helper.get_serializer_cls import (
    user_session_serializer_class,
)
from user_behavior.models import UserInteraction, UserSession


class UserInteractionSerializer(serializers.ModelSerializer):
    session_id = serializers.CharField(
        write_only=True,
        label=_("User Session session_id"),
        help_text=_(
            "The session_id of the user session during which this interaction occurred."
        ),
    )
    session = user_session_serializer_class()(read_only=True)

    class Meta:
        model = UserInteraction
        fields = ["id", "session_id", "session", "event_type", "element", "metadata"]
        read_only_fields = ("timestamp",)

    def validate_session_id(self, value):
        user_session = UserSession.objects.filter(session_id=value).first()
        if not user_session:
            raise serializers.ValidationError(_("User with this session ID not found"))
        return user_session

    def create(self, validated_data):
        session = validated_data.get("session_id")
        event_type = validated_data.get("event_type")
        element = validated_data.get("element")
        metadata = (
            validated_data.get("metadata") if validated_data.get("metadata") else {}
        )

        user_interaction = UserInteraction()
        user_interaction.session = session
        user_interaction.event_type = event_type
        user_interaction.element = element
        user_interaction.metadata = metadata
        user_interaction.save()

        return user_interaction
