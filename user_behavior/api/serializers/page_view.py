from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from user_behavior.models import PageView, UserSession

from .helper.get_serializer_cls import user_session_serializer_class


class PageViewSerializer(serializers.ModelSerializer):
    session_id = serializers.CharField(
        write_only=True,
        label=_("User Session session_id"),
        help_text=_(
            "The session_id of the user session during which this page view occurred."
        ),
    )
    session = user_session_serializer_class()(read_only=True)

    class Meta:
        model = PageView
        fields = ["id", "url", "timestamp", "session_id", "session"]
        read_only_fields = ("timestamp",)

    def validate_session_id(self, value):
        user_session = UserSession.objects.filter(session_id=value).first()
        if not user_session:
            raise serializers.ValidationError(_("User with this session ID not found"))
        return user_session

    def create(self, validated_data):
        session = validated_data.get("session_id")
        url = validated_data.get("url")

        page_view = PageView()
        page_view.url = url
        page_view.session = session
        page_view.save()

        return page_view
