from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core import serializers, permissions
from drf_spectacular.utils import extend_schema


class WelcomeMessage(APIView):
    """Just a warm welcome message"""

    @extend_schema(tags=["project info"])
    def get(self, request):
        return Response(
            {"response": "welcome to my Django Rest Framework application"},
            status.HTTP_200_OK,
        )


class SignupView(APIView):
    """The signup endpoint APIView"""

    serializer_class = serializers.SignupSerializer
    permission_classes = [permissions.IsAnonymous]

    @extend_schema(tags=["core authentication"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()

        return Response(response, status.HTTP_201_CREATED)


class LoginView(APIView):
    """The login endpoint APIView"""

    serializer_class = serializers.LoginSerializer
    permission_classes = [permissions.IsAnonymous]

    @extend_schema(tags=["core authentication"])
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()

        return Response(response, status.HTTP_202_ACCEPTED)
