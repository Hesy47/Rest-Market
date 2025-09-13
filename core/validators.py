from rest_framework import serializers
import re


def username_validator(value: str):
    """The general validation rules for username field"""

    if not value.isalnum():
        raise serializers.ValidationError("The username must be alphanumeric")

    return value


def phone_number_validator(value: str):
    """The general validation rules for phone number field"""

    if not value.isdigit():
        raise serializers.ValidationError("The phone number must be only digits")

    if len(value) != 11:
        raise serializers.ValidationError("The phone number must be exactly 11 digits")

    return value


def password_validator(value: str):
    """The general validation rules for password field"""

    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$"

    if not bool(re.match(pattern, value)):
        raise serializers.ValidationError(
            "The password must contain one uppercase letter, "
            "one lowercase letter and one number"
        )

    return value
