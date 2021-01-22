from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

__all__ = (
    'validate_password',
)


def validate_user_password(value):
    try:
        validate_password(value)
    except ValidationError as e:
        raise serializers.ValidationError(e.messages)
    return value
