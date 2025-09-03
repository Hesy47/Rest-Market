from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from core import validators


class SignupSerializer(serializers.Serializer):
    """The signup endpoint serializer"""

    email = serializers.EmailField(
        max_length=60,
        required=True,
        validators=[
            UniqueValidator(
                queryset=get_user_model().objects.all(),
                message="This email address is already in use",
            )
        ],
        error_messages={
            "max_length": "The email address can be at most 60 characters",
            "invalid": "Please enter a valid email address",
            "required": "The email address field is required",
        },
    )

    username = serializers.CharField(
        max_length=30,
        min_length=5,
        required=True,
        validators=[
            validators.username_validator,
            UniqueValidator(
                queryset=get_user_model().objects.all(),
                message="This username is already in use",
            ),
        ],
        error_messages={
            "max_length": "The username can be at most 30 characters",
            "min_length": "The username must be at least 5 characters",
        },
    )

    phone_number = serializers.CharField(
        required=True,
        validators=[
            validators.phone_number_validator,
            UniqueValidator(
                queryset=get_user_model().objects.all(),
                message="This phone number is already in use",
            ),
        ],
        error_messages={
            "max_length": "The phone number can be at most 11 characters",
            "required": "The phone number field is required",
        },
    )

    password = serializers.CharField(
        max_length=24,
        min_length=8,
        required=True,
        write_only=True,
        validators=[validators.password_validator],
        error_messages={
            "max_length": "The password can be at most 24 characters long",
            "min_length": "The password must be at least 8 characters long",
            "required": "The password field is required",
        },
    )

    password_confirmation = serializers.CharField(
        required=True,
        write_only=True,
    )

    def validate(self, attrs: dict):
        password = attrs.get("password")
        password_confirmation = attrs.get(password_confirmation)

        if password != password_confirmation:
            raise serializers.ValidationError(
                "password and password confirmation must be"
            )

    def create(self, validated_data):
        new_user = get_user_model().objects.create_user(**validated_data)

        return {
            "response": f"user with the username of: {new_user.username} "
            f"and id of: {new_user.id} has been created successfully"
        }


class LoginSerializer(serializers.Serializer):
    """The login endpoint serializer"""

    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "The email field must not be empty",
            "blank": "The email field must not be empty",
            "invalid": "please inter a valid email address",
        },
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
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
