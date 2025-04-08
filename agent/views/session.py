import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from commons.domain.utils.utils import generate_uuid
from agent.models import Session
from agent.domain.entities.GenerateSessionRequest import GenerateSessionRequest

@method_decorator(csrf_exempt, name='dispatch')
class SessionAPI(APIView):

    authentication_classes = []     
    permission_classes = []
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        try:
            generate_session_request = GenerateSessionRequest(**request.data)
            session_id = generate_uuid()
            Session.objects.create(email=generate_session_request.email, uuid = session_id)

            response_data = {
                "session_id": session_id
            }

            return Response(
                response_data,
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "error": "Error uploading file to cloud storage",
                    "details": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )