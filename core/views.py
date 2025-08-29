from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class WelcomeMessage(APIView):
    """Just a warm welcome message"""

    def get(self, request):
        return Response(
            {"response": "welcome to my Django Rest Framework application"},
            status.HTTP_200_OK,
        )
