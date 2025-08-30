from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core import serializers, permissions


class WelcomeMessage(APIView):
    """Just a warm welcome message"""

    def get(self, request):
        return Response(
            {"response": "welcome to my Django Rest Framework application"},
            status.HTTP_200_OK,
        )


class LoginView(APIView):
    """The login endpoint APIView"""

    serializer_class = serializers.LoginSerializer
    permission_classes = [permissions.IsAnonymous]

    def post(self, request):
        # user = request.user
        # print(user)
        # if user != "AnonymousUser":
        #     return Response(
        #         {"response": "please logout from your current account"},
        #         status.HTTP_403_FORBIDDEN,
        #     )

        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()

        return Response(response, status.HTTP_202_ACCEPTED)
