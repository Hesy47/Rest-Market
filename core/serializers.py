from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


class SignupSerializer(serializers.Serializer):
    """The signup endpoint serializer"""

    email = serializers.EmailField(
        max_length=60,
        validators=[
            UniqueValidator(
                queryset=get_user_model().objects.all(),
                message="This email address is already in use"
            )
        ],
        error_messages={
            "max_length": "The email address can be at most 60 characters",
            "invalid": "Please enter a valid email address"
        },
    )

    username = serializers.CharField(
        max_length=30,
        min_length=5,
        validators=[
            UniqueValidator(
                queryset=get_user_model().objects.all(),
                message="This username is already in use"),
        ],
        error_messages={
            "max_length": "The username can be at most 30 characters",
            "min_length": "The username must be at least 5 characters"
        },

    )

    phone_number = serializers.CharField(
        max_length=11,
        validators=[
            UniqueValidator(
                queryset=get_user_model().objects.all(),
                message="This phone number is already in use")
        ],
        error_messages={"max_length": "The phone number can be at most 11 characters"}
    )


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
