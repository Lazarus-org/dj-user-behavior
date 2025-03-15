from typing import List, Optional, Type, Dict, Any, Union

from rest_framework.pagination import BasePagination
from rest_framework.parsers import BaseParser
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework.throttling import BaseThrottle

from user_behavior.settings.conf import config


class ConfigureAttrsMixin:
    """
    A mixin for dynamically configuring API attributes based on settings.
    Supports both global defaults and viewset-specific configurations.

    Attributes:
        config_prefix (str): Prefix for config attributes specific to this viewset
        default_config (Dict[str, Any]): Default configuration values
    """

    # Prefix for viewset-specific config attributes (to be overridden in subclass)
    config_prefix: str = ""

    # Default configuration values
    default_config: Dict[str, Any] = {
        "ordering_fields": None,
        "search_fields": None,
        "parser_classes": [],
        "permission_classes": [AllowAny],
        "filterset_class": None,
        "pagination_class": None,
        "throttle_classes": [],
        "extra_permission_class": None,
    }

    def configure_attrs(self) -> None:
        """
        Configures API attributes dynamically based on settings from config.
        Uses viewset-specific settings when available, falling back to global defaults.
        """
        # Get viewset-specific config attribute names
        specific_ordering = (
            f"api_{self.config_prefix}_ordering_fields"
            if self.config_prefix
            else "api_ordering_fields"
        )
        specific_search = (
            f"api_{self.config_prefix}_search_fields"
            if self.config_prefix
            else "api_search_fields"
        )
        specific_parsers = (
            f"api_{self.config_prefix}_parser_classes"
            if self.config_prefix
            else "api_parser_classes"
        )
        specific_permissions = (
            f"api_{self.config_prefix}_extra_permission_class"
            if self.config_prefix
            else "api_extra_permission_class"
        )
        specific_filterset = (
            f"api_{self.config_prefix}_filterset_class"
            if self.config_prefix
            else "api_filterset_class"
        )
        specific_pagination = (
            f"api_{self.config_prefix}_pagination_class"
            if self.config_prefix
            else "api_pagination_class"
        )
        specific_throttle = (
            f"api_{self.config_prefix}_throttle_classes"
            if self.config_prefix
            else "api_throttle_classes"
        )

        # Set ordering fields
        self.ordering_fields: Optional[List[str]] = (
            getattr(config, specific_ordering, None)
            if hasattr(config, specific_ordering)
            else getattr(
                config, "api_ordering_fields", self.default_config["ordering_fields"]
            )
        )

        # Set search fields
        self.search_fields: Optional[List[str]] = (
            getattr(config, specific_search, None)
            if hasattr(config, specific_search)
            else getattr(
                config, "api_search_fields", self.default_config["search_fields"]
            )
        )

        # Set parser classes
        self.parser_classes: List[Type[BaseParser]] = (
            getattr(config, specific_parsers, [])
            if hasattr(config, specific_parsers)
            else getattr(
                config, "api_parser_classes", self.default_config["parser_classes"]
            )
        )

        # Set permission classes
        self.permission_classes: List[Type[BasePermission]] = list(
            self.default_config["permission_classes"]
        )
        extra_perm = (
            getattr(config, specific_permissions, None)
            if hasattr(config, specific_permissions)
            else getattr(
                config,
                "api_extra_permission_class",
                self.default_config["extra_permission_class"],
            )
        )
        if extra_perm:
            self.permission_classes.append(extra_perm)

        # Set filterset class
        self.filterset_class = (
            getattr(config, specific_filterset, None)
            if hasattr(config, specific_filterset)
            else getattr(
                config, "api_filterset_class", self.default_config["filterset_class"]
            )
        )

        # Set pagination class
        self.pagination_class: Optional[Type[BasePagination]] = (
            getattr(config, specific_pagination, None)
            if hasattr(config, specific_pagination)
            else getattr(
                config, "api_pagination_class", self.default_config["pagination_class"]
            )
        )

        # Set throttle classes
        throttle_setting = (
            getattr(config, specific_throttle, None)
            if hasattr(config, specific_throttle)
            else getattr(
                config, "api_throttle_classes", self.default_config["throttle_classes"]
            )
        )
        self.throttle_classes: List[Type[BaseThrottle]] = (
            self._normalize_throttle_classes(throttle_setting)
        )

    def _normalize_throttle_classes(
        self,
        throttle_setting: Union[Type[BaseThrottle], List[Type[BaseThrottle]], None],
    ) -> List[Type[BaseThrottle]]:
        """
        Normalizes throttle settings into a list of throttle classes.

        Args:
            throttle_setting: Can be a single throttle class, a list of throttle classes, or None.

        Returns:
            A list of throttle classes.
        """
        if throttle_setting is None:
            return self.default_config["throttle_classes"]
        elif isinstance(throttle_setting, (list, tuple)):
            return [cls for cls in throttle_setting if issubclass(cls, BaseThrottle)]
        elif issubclass(throttle_setting, BaseThrottle):
            return [throttle_setting]
        else:
            raise ValueError(
                f"Invalid throttle setting: {throttle_setting}. Must be a BaseThrottle subclass or list of subclasses."
            )
