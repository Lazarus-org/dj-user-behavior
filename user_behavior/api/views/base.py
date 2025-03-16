from typing import List, Optional, Type

from rest_framework import filters, viewsets
from rest_framework.serializers import Serializer

from user_behavior.mixins.api.config_api_attrs import ConfigureAttrsMixin
from user_behavior.mixins.api.control_api_methods import ControlAPIMethodsMixin
from user_behavior.settings.conf import config

try:
    from django_filters.rest_framework import DjangoFilterBackend

    django_filter_installed = True
except ImportError:  # pragma: no cover
    django_filter_installed = False


class BaseViewSet(viewsets.GenericViewSet, ConfigureAttrsMixin, ControlAPIMethodsMixin):
    """A base viewset class that provides common functionality for filtering,
    ordering, and method control with initialization configuration."""

    # Default filter backends
    filter_backends: List = [
        *([DjangoFilterBackend] if django_filter_installed else []),
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    # Class attributes to be overridden by subclasses
    queryset = None
    serializer_class: Optional[Type[Serializer]] = None

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the viewset and configure attributes based on settings.

        Disables the 'list', 'retrieve', 'create', 'update', and 'destroy' methods
        if their corresponding settings are set to `False`.

        """
        super().__init__(*args, **kwargs)
        self.configure_attrs()

        # Mapping of configuration settings to the corresponding methods to disable
        config_method_mapping = {
            "api_allow_list": "LIST",
            "api_allow_retrieve": "RETRIEVE",
            "api_allow_create": "CREATE",
            "api_allow_update": "UPDATE",
            "api_allow_delete": "DESTROY",
        }

        for config_setting, method in config_method_mapping.items():
            if not getattr(config, config_setting, True):
                self.disable_methods([method])

    def get_queryset(self):
        """Get the queryset for the viewset.

        Can be overridden in subclasses for custom queryset logic.

        """
        if self.queryset is None:
            raise AssertionError("queryset must be defined in the subclass")
        return self.queryset

    def get_serializer_class(self):
        """Get the serializer class for the viewset.

        Can be overridden in subclasses for custom serializer logic.

        """
        if self.serializer_class is None:
            raise AssertionError("serializer_class must be defined in the subclass")
        return self.serializer_class
