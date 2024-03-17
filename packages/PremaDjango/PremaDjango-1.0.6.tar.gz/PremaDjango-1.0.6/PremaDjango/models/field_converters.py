"""Module containing custom field converters for Django models."""

from django.db import models


class LowercaseCharField(models.CharField):
    """Lowercases the input value."""

    def get_prep_value(self, value):
        """Lowercase the value."""
        value = super().get_prep_value(value)
        if value is not None:
            value = value.lower()
        return value


class UppercaseCharField(models.CharField):
    """Uppercases the input value."""

    def get_prep_value(self, value):
        """Uppercase the value."""
        value = super().get_prep_value(value)
        if value is not None:
            value = value.upper()
        return value


class TitleCaseCharField(models.CharField):
    """Title cases the input value."""

    def get_prep_value(self, value):
        """Title case the value."""
        value = super().get_prep_value(value)
        if value is not None:
            value = value.title()
        return value


class CamelCaseCharField(models.CharField):
    """Converts the input value to camel case."""

    def get_prep_value(self, value):
        """Convert value to camel case."""
        value = super().get_prep_value(value)
        if value is not None:
            value = "".join(word.capitalize() for word in value.split())
        return value


class SnakeCaseCharField(models.CharField):
    """Converts the input value to snake case."""

    def get_prep_value(self, value):
        """Convert value to snake case."""
        value = super().get_prep_value(value)
        if value is not None:
            value = "_".join(word.lower() for word in value.split())
        return value
