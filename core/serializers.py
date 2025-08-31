from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth import authenticate


class SignupSerializer(serializers.Serializer):
    pass


class LoginSerializer(serializers.Serializer):
    """The login endpoint serializer"""

    email = serializers.EmailField(
        required=True,
        write_only=True,
        error_messages={
            "required": "The email field must not be empty",
            "blank": "The email field must not be empty",
            "invalid": "please inter a valid email address",
        },
    )

    password = serializers.CharField(
        required=True,
        style={"input_type": "password"},
        error_messages={
            "required": "The password field must not be empty",
            "blank": "The password field must not be empty",
        },
    )

    def validate(self, attrs: dict):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid email or password")

        attrs["user"] = user

        return attrs

    def create(self, validated_data: dict):
        user = validated_data.get("user")

        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        return {
            "access_token": str(access_token),
            "refresh_token": str(refresh_token),
        }
