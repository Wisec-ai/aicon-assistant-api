import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Document

@method_decorator(csrf_exempt, name='dispatch')
class AgentConversationAPI(APIView):

    authentication_classes = []     
    permission_classes = []
    throttle_classes = [AnonRateThrottle]

    def post(self, request):

        try:
            pass
            
            return Response(
                {
                    "exit": "",
                    "details": "",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:

            return Response(
                {
                    "error": "Error uploading file to cloud storage",
                    "details": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )