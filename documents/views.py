import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .domain.models.document_info import DocumentInfo
from .application.service import Service

@method_decorator(csrf_exempt, name='dispatch')
class DocumentListAPI(APIView):

    authentication_classes = []     
    permission_classes = []
    throttle_classes = [AnonRateThrottle]

    def post(self, request):

        try:
            document_info = DocumentInfo(**request.data)
            Service.load_data_pubsub(document_info.file_name)
            return Response(
                {
                    "status": "Successful",
                    "details": "",
                },
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