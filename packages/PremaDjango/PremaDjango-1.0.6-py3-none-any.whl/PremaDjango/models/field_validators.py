"""Module containing custom field validators for Django models."""

import re

from django.core.exceptions import ValidationError


def first_letter_char_validator(value):
    """Validate that the first letter is a character."""
    if not value[0].isalpha():
        raise ValidationError("First letter must be a character.")


def first_letter_int_validator(value):
    """Validate that the first letter is an integer."""
    try:
        int(value[0])
    except ValueError:
        raise ValidationError("First letter must be an integer.")


def first_letter_special_char_validator(value):
    """Validate that the first letter is a special character."""
    if not re.match(r"^[^a-zA-Z0-9]", value[0]):
        raise ValidationError("First letter must be a special character.")


def min_length_validator(min_length=10):
    """Validate that a given number of characters are within the minimum length."""

    def validator(value):
        if len(value) < min_length:
            raise ValidationError(f"The length must be at least {min_length} characters.")

    return validator


def max_length_validator(max_length=50):
    """Validate that a given number of characters are within the maximum length."""

    def validator(value):
        if len(value) > max_length:
            raise ValidationError(f"The length must be at most {max_length} characters.")

    return validator


def min_and_max_length_validator(min_length=8, max_length=100):
    """Validate that a given number of characters are within the minimum and maximum length."""

    def validator(value):
        if len(value) < min_length:
            raise ValidationError(f"The length must be at least {min_length} characters.")
        elif len(value) > max_length:
            raise ValidationError(f"The length must be at most {max_length} characters.")

    return validator


def no_special_char_validator(value):
    """Validate that there are no special characters."""
    if not value.isalnum():
        raise ValidationError("Special characters are not allowed.")


def no_numbers_validator(value):
    """Validate that there are no numbers."""
    if any(char.isdigit() for char in value):
        raise ValidationError("Numbers are not allowed.")


def no_characters_validator(value):
    """Validate that there are no characters."""
    if any(char.isalpha() for char in value):
        raise ValidationError("Characters are not allowed.")


def at_least_n_characters_validator(min_characters=1):
    """Validate that there are at least n characters."""

    def validator(value):
        if not any(char.isalpha() for char in value):
            raise ValidationError(f"At least {min_characters} character(s) is required.")

    return validator


def at_least_one_number_validator(min_numbers=1):
    """Check if at least one number is required for a given number of characters."""

    def validator(value):
        if sum(char.isdigit() for char in value) < min_numbers:
            raise ValidationError(f"At least {min_numbers} numeric character(s) is required.")

    return validator


def at_least_one_special_char_validator(min_special_chars=1):
    """Check if at least one special character is required for a given number of characters."""

    def validator(value):
        if sum(not char.isalnum() for char in value) < min_special_chars:
            raise ValidationError(f"At least {min_special_chars} special character(s) is required.")

    return validator


def allowed_characters_validator(allowed_chars):
    """Validate that only the given characters are allowed."""

    def validator(value):
        for char in value:
            if char not in allowed_chars:
                raise ValidationError(f"Only the following characters are allowed: {', '.join(allowed_chars)}")

    return validator


def disallowed_characters_validator(disallowed_chars):
    """Check if any disallowed character is present."""

    def validator(value):
        for char in value:
            if char in disallowed_chars:
                raise ValidationError(f"Character '{char}' is not allowed.")

    return validator


def indian_mobile_validator(value):
    """Validate Indian mobile numbers."""
    if not str(value).isdigit():
        raise ValidationError("Mobile number must contain only digits.")
    if len(str(value)) != 10:
        raise ValidationError("Mobile number must contain exactly 10 digits.")
    if str(value)[0] not in ['9', '8', '7', '6']:
        raise ValidationError("Mobile number must start with 9, 8, 7, or 6.")
